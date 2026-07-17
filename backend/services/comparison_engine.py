import difflib
import uuid
from typing import List, Set
from backend.models.schemas import (
    ComparisonResult, MatchClassification, DiffLine,
    AttributionData, PurchaseSalesData, GeneratedCommentary
)


class ComparisonEngine:
    """Compares lead account vs sub-account and computes match score."""

    WEIGHTS = {
        "holdings_overlap": 0.40,
        "performance_match": 0.25,
        "transaction_overlap": 0.20,
        "narrative_match": 0.15
    }

    def compare(
        self,
        account_id: str,
        lead_account_id: str,
        lead_attribution: AttributionData,
        account_attribution: AttributionData,
        lead_ps: PurchaseSalesData,
        account_ps: PurchaseSalesData,
        lead_commentary: GeneratedCommentary,
        account_commentary: GeneratedCommentary
    ) -> ComparisonResult:

        # ── Component Scores ────────────────────────────────
        holdings = self._holdings_overlap(lead_attribution, account_attribution)
        performance = self._performance_match(lead_attribution, account_attribution)
        transaction = self._transaction_overlap(lead_ps, account_ps)
        narrative = self._narrative_match(lead_commentary, account_commentary)

        # ── Weighted Score ──────────────────────────────────
        match_score = (
            holdings * self.WEIGHTS["holdings_overlap"] +
            performance * self.WEIGHTS["performance_match"] +
            transaction * self.WEIGHTS["transaction_overlap"] +
            narrative * self.WEIGHTS["narrative_match"]
        ) * 100

        match_score = round(min(max(match_score, 0), 100), 2)
        classification = self._classify(match_score)

        # ── Diff Lines ──────────────────────────────────────
        diff_lines = self._compute_diff(lead_commentary, account_commentary)

        return ComparisonResult(
            account_id=account_id,
            lead_account_id=lead_account_id,
            match_score=match_score,
            classification=classification,
            holdings_overlap=round(holdings * 100, 2),
            performance_match=round(performance * 100, 2),
            transaction_overlap=round(transaction * 100, 2),
            narrative_match=round(narrative * 100, 2),
            diff_lines=diff_lines
        )

    def _holdings_overlap(
        self,
        lead: AttributionData,
        account: AttributionData
    ) -> float:
        lead_names: Set[str] = {
            c.security_name.lower()
            for c in lead.top_contributors + lead.bottom_contributors
        }
        acct_names: Set[str] = {
            c.security_name.lower()
            for c in account.top_contributors + account.bottom_contributors
        }
        if not lead_names:
            return 0.5
        intersection = lead_names & acct_names
        union = lead_names | acct_names
        return len(intersection) / len(union) if union else 0.0

    def _performance_match(
        self,
        lead: AttributionData,
        account: AttributionData
    ) -> float:
        lead_ret = lead.total_portfolio_return
        acct_ret = account.total_portfolio_return
        if lead_ret == 0:
            return 1.0 if acct_ret == 0 else 0.5
        diff = abs(lead_ret - acct_ret)
        # Within 0.5% = high match
        score = max(0.0, 1.0 - (diff / 2.0))
        return min(score, 1.0)

    def _transaction_overlap(
        self,
        lead: PurchaseSalesData,
        account: PurchaseSalesData
    ) -> float:
        lead_names: Set[str] = {
            t.security_name.lower()
            for t in lead.purchases + lead.sales
        }
        acct_names: Set[str] = {
            t.security_name.lower()
            for t in account.purchases + account.sales
        }
        if not lead_names:
            return 0.8  # Assume overlap if lead has no transactions
        if not acct_names:
            return 0.5
        intersection = lead_names & acct_names
        union = lead_names | acct_names
        return len(intersection) / len(union) if union else 0.0

    def _narrative_match(
        self,
        lead: GeneratedCommentary,
        account: GeneratedCommentary
    ) -> float:
        lead_text = " ".join(
            s.content for s in lead.sections if s.is_auto_generated
        ).lower()
        acct_text = " ".join(
            s.content for s in account.sections if s.is_auto_generated
        ).lower()

        if not lead_text or not acct_text:
            return 0.5

        sm = difflib.SequenceMatcher(None, lead_text, acct_text)
        return sm.ratio()

    def _classify(self, score: float) -> MatchClassification:
        if score >= 95:
            return MatchClassification.MIRROR
        elif score >= 80:
            return MatchClassification.MINOR
        elif score >= 60:
            return MatchClassification.MODERATE
        else:
            return MatchClassification.SIGNIFICANT

    def _compute_diff(
        self,
        lead: GeneratedCommentary,
        account: GeneratedCommentary
    ) -> List[DiffLine]:
        lead_text = "\n".join(s.content for s in lead.sections)
        acct_text = "\n".join(s.content for s in account.sections)

        lead_lines = lead_text.splitlines()
        acct_lines = acct_text.splitlines()

        diff_lines: List[DiffLine] = []
        sm = difflib.SequenceMatcher(None, lead_lines, acct_lines)

        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == 'equal':
                for line in lead_lines[i1:i2]:
                    diff_lines.append(DiffLine(
                        line_type="equal",
                        lead_text=line,
                        account_text=line
                    ))
            elif tag == 'replace':
                for lead_line, acct_line in zip(
                    lead_lines[i1:i2], acct_lines[j1:j2]
                ):
                    diff_lines.append(DiffLine(
                        line_type="replace",
                        lead_text=lead_line,
                        account_text=acct_line
                    ))
            elif tag == 'insert':
                for line in acct_lines[j1:j2]:
                    diff_lines.append(DiffLine(
                        line_type="insert",
                        lead_text=None,
                        account_text=line
                    ))
            elif tag == 'delete':
                for line in lead_lines[i1:i2]:
                    diff_lines.append(DiffLine(
                        line_type="delete",
                        lead_text=line,
                        account_text=None
                    ))
        return diff_lines
import re
import uuid
from typing import Dict, Optional
from backend.models.schemas import (
    GeneratedCommentary, CommentarySection,
    AttributionData, PurchaseSalesData,
    PerformanceRecord, ProcessingStatus
)


class CommentaryEngine:
    """Generates account-level commentary by populating template sections."""

    def generate(
        self,
        account_id: str,
        strategy_id: str,
        period: str,
        lead_commentary: Dict,
        attribution: Optional[AttributionData],
        purchase_sales: Optional[PurchaseSalesData],
        performance: Optional[PerformanceRecord]
    ) -> GeneratedCommentary:

        sections = []

        # ── 1. Strategy Overview ────────────────────────────
        overview_text = self._get_section(
            lead_commentary, ["overview", "strategy", "introduction"]
        )
        if overview_text:
            sections.append(CommentarySection(
                section_name="Strategy Overview",
                content=overview_text,
                is_auto_generated=False   # Sourced from lead doc
            ))

        # ── 2. Performance Summary ──────────────────────────
        perf_text = self._build_performance_section(performance, attribution)
        sections.append(CommentarySection(
            section_name="Performance Summary",
            content=perf_text,
            is_auto_generated=True
        ))

        # ── 3. Attribution Analysis ─────────────────────────
        if attribution:
            attr_text = self._build_attribution_section(attribution)
            sections.append(CommentarySection(
                section_name="Attribution Analysis",
                content=attr_text,
                is_auto_generated=True
            ))

        # ── 4. Transaction Activity ─────────────────────────
        if purchase_sales:
            txn_text = self._build_transaction_section(purchase_sales)
            sections.append(CommentarySection(
                section_name="Transaction Activity",
                content=txn_text,
                is_auto_generated=True
            ))

        # ── 5. Portfolio Positioning ────────────────────────
        positioning_text = self._get_section(
            lead_commentary, ["position", "outlook", "market"]
        )
        if positioning_text:
            # Replace any generic placeholders
            positioning_text = self._inject_values(
                positioning_text,
                account_id=account_id,
                performance=performance
            )
            sections.append(CommentarySection(
                section_name="Portfolio Positioning & Outlook",
                content=positioning_text,
                is_auto_generated=False
            ))

        return GeneratedCommentary(
            commentary_id=str(uuid.uuid4()),
            account_id=account_id,
            strategy_id=strategy_id,
            period=period,
            sections=sections,
            status=ProcessingStatus.REVIEW
        )

    # ── Section Helpers ─────────────────────────────────────
    def _get_section(
        self, lead_doc: Dict, keywords: list
    ) -> Optional[str]:
        """Find a section from lead commentary matching keywords."""
        sections = lead_doc.get("sections", {})
        for key, content in sections.items():
            if any(kw in key.lower() for kw in keywords):
                return content
        # Fall back to full text excerpt
        full = lead_doc.get("full_text", "")
        if full:
            return full[:500] + "..." if len(full) > 500 else full
        return None

    def _inject_values(
        self,
        text: str,
        account_id: str,
        performance: Optional[PerformanceRecord]
    ) -> str:
        """Replace [placeholder] tokens with real values."""
        replacements = {
            "Account Name": account_id,
            "Account ID": account_id,
            "Period": performance.period if performance else "4Q25",
            "Portfolio Return": (
                f"{performance.portfolio_return:.2f}%"
                if performance else "N/A"
            ),
            "Benchmark Return": (
                f"{performance.benchmark_return:.2f}%"
                if performance else "N/A"
            ),
            "Active Return": (
                f"{performance.active_return:.2f}%"
                if performance else "N/A"
            ),
        }
        for placeholder, value in replacements.items():
            text = re.sub(
                rf'\[{re.escape(placeholder)}\]',
                value, text, flags=re.IGNORECASE
            )
        return text

    def _build_performance_section(
        self,
        performance: Optional[PerformanceRecord],
        attribution: Optional[AttributionData]
    ) -> str:
        if not performance and not attribution:
            return "Performance data not available for this account."

        if attribution:
            port_ret = attribution.total_portfolio_return
            bench_ret = attribution.total_benchmark_return
            active = attribution.total_active_return
            benchmark = attribution.benchmark_name
            period = attribution.period
        elif performance:
            port_ret = performance.portfolio_return
            bench_ret = performance.benchmark_return
            active = performance.active_return
            benchmark = "Benchmark Index"
            period = performance.period
        else:
            return "Performance data unavailable."

        direction = "outperformed" if active > 0 else "underperformed"
        abs_active = abs(active)

        text = (
            f"For the period ending {period}, the portfolio returned {port_ret:.2f}%, "
            f"compared to the {benchmark} return of {bench_ret:.2f}%. "
            f"The portfolio {direction} the benchmark by {abs_active:.2f}% "
            f"on a gross of fees basis."
        )
        return text

    def _build_attribution_section(self, attribution: AttributionData) -> str:
        lines = [
            f"For the {attribution.period} period, the following securities "
            f"were among the primary drivers of relative performance "
            f"versus the {attribution.benchmark_name}.",
            "",
            "Top Contributors:"
        ]

        for c in attribution.top_contributors[:3]:
            if c.contribution > 0:
                lines.append(
                    f"  • {c.security_name}: contributed +{c.contribution:.2f}% "
                    f"to relative performance."
                )

        if attribution.bottom_contributors:
            lines.append("")
            lines.append("Primary Detractors:")
            for c in attribution.bottom_contributors[:3]:
                lines.append(
                    f"  • {c.security_name}: detracted {c.contribution:.2f}% "
                    f"from relative performance."
                )

        return "\n".join(lines)

    def _build_transaction_section(
        self, ps: PurchaseSalesData
    ) -> str:
        lines = []

        if ps.purchases:
            lines.append("During the period, the following positions were initiated or added:")
            lines.append("")
            for p in ps.purchases[:5]:
                lines.append(f"  Purchased: {p.security_name}")
                if p.rationale and p.rationale != "No rationale provided.":
                    lines.append(f"  Rationale: {p.rationale}")
                lines.append("")

        if ps.sales:
            if lines:
                lines.append("")
            lines.append("The following positions were reduced or exited:")
            lines.append("")
            for s in ps.sales[:5]:
                lines.append(f"  Sold: {s.security_name}")
                if s.rationale and s.rationale != "No rationale provided.":
                    lines.append(f"  Rationale: {s.rationale}")
                lines.append("")

        if not lines:
            return "No transaction activity recorded for this period."

        return "\n".join(lines)
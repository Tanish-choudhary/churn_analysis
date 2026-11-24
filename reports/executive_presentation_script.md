# Executive Presentation Script

**Project:** Executive Analytics Capstone — Customer Churn Analysis & Retention Prioritization
**Presenter:** [Your Name], Executive Analytics Capstone Intern
**Target Duration:** ~10 minutes (10 slides)
**Audience:** Senior Leadership, Customer Retention Division

---

## Slide 1: Title & Business Objective
**Estimated Duration: 45 seconds**

**Key Points:**
- Good morning/afternoon. I'm [Name], presenting our Executive Analytics Capstone on Customer Churn Analysis and Retention Prioritization.
- This project was completed as part of my internship with the Executive Analytics team.
- Our business objective is clear: identify vulnerable customer segments, prioritize retention resources, and enable data-informed decisions using transparent, explainable analytics — not black-box predictions.

**Transition:** "Let me start by framing why this problem matters to the business."

---

## Slide 2: The Business Problem
**Estimated Duration: 60 seconds**

**Key Points:**
- Customer churn isn't just a metric — it's a direct hit to revenue. Every lost customer is lost recurring revenue.
- The acquisition cost asymmetry is critical: new customers cost 5 to 25 times more to acquire than retaining existing ones.
- Churned customers don't just disappear — they often go to competitors, taking their lifetime value with them.
- High sustained churn is also a brand signal that we have systemic unmet needs.
- Our key business questions: Who is most likely to leave? What defines vulnerable segments? Where should we focus limited resources? What actions address root causes? How do we measure impact?

**Transition:** "To answer these questions reliably, we need a solid data foundation."

---

## Slide 3: Data Quality & Analytical Foundation
**Estimated Duration: 60 seconds**

**Key Points:**
- We started with 10,100 raw records and cleaned to 10,000 records after removing duplicates and standardizing data types.
- Missing values were imputed conservatively: median for charges, mode for categoricals.
- Outliers were flagged but preserved — we didn't delete data, we made it transparent.
- The overall churn rate is 75.06% with a 24.94% retention rate, and $688,744 in monthly recurring revenue.

**Critical principle:** We never used the Churn target to create segments or risk scores. It was excluded entirely and only used afterward for validation. This prevents data leakage and ensures our segmentation is purely descriptive.

**Analytical pipeline:** Exploratory analysis → Interactive KPI Dashboard → K-Means segmentation (4 segments) → Rule-based risk scoring (7 transparent factors) → Validation via historical churn rates.

**Transition:** "Let's look at what the exploratory analysis revealed about churn drivers."

---

## Slide 4: Key Findings from Exploratory Analysis
**Estimated Duration: 75 seconds**

**Key Points:**
- **Contract type:** Surprisingly minimal differentiation. Month-to-month at 74.7%, Two-year at 75.5%. All contract types show high churn — contract alone isn't the story.
- **Tenure:** Not protective as we might hope. Lowest quartile (0-12 months) churns at 75.9%, highest quartile (50+ months) at 76.8%. Tenure alone doesn't prevent churn.
- **Payment method matters:** Electronic check users are overrepresented in High Risk. Auto-pay correlates with stability.
- **Service gaps:** Customers without online security have elevated risk scores (+10 points in our model).
- **Senior citizens form a unique cluster:** 100% of our Senior Vulnerable segment are seniors — they have a distinct risk profile.

**Transition:** "These patterns informed our interactive dashboard for ongoing monitoring."

---

## Slide 5: Business KPI Dashboard
**Estimated Duration: 45 seconds**

**Key Points:**
- We built an interactive Streamlit dashboard (`app.py`) for real-time monitoring.
- Key KPIs: 75.06% churn rate, 24.94% retention, $155,849 monthly revenue at risk from High-Risk customers.
- Filters allow slicing by contract type, tenure range, and monthly charges — KPIs update instantly.
- Visualizations include churn by contract, tenure distribution, revenue at risk, and customer segmentation.
- Auto-generated business insights adapt to the filtered view.

**Transition:** "The dashboard monitors the 'what.' Segmentation explains the 'who.'"

---

## Slide 6: Customer Segmentation
**Estimated Duration: 90 seconds**

**Key Points:**
- Using K-Means on 9 features (financial, service, payment, demographic — no Churn), we identified 4 segments.
- **Senior Vulnerable** (1,546 customers, 15.5%): 100% seniors, month-to-month, electronic check, no security. Highest % High Risk at 25.9%.
- **Budget-Conscious** (3,151 customers, 31.5%): Largest segment, lowest charges ($59.49), mailed check, has security. Risk driven by contract and payment.
- **High-Value Long-Term** (2,343 customers, 23.4%): Highest tenure (56 months), highest charges ($91.76), highest lifetime value ($5,092). Despite loyalty signals, 76.2% historical churn — revenue protection is critical.
- **New Vulnerable** (2,960 customers, 29.6%): Lowest tenure (28 months), auto-pay, no security. Early intervention opportunity.

**Transition:** "Segments describe groups. Risk scoring prioritizes individuals within them."

---

## Slide 7: Risk Prioritization
**Estimated Duration: 75 seconds**

**Key Points:**
- We built a transparent rule-based score from 0-100 using 7 business-relevant factors — no machine learning black box.
- Factors: Short tenure (max 25), high monthly charges (max 20), month-to-month contract (max 25), manual payment (max 10), no online security (max 10), senior citizen (5), no partner/dependents (5).
- Categories: Low (0-34): 27.9%, Medium (35-59): 53.7%, High (60-100): 18.3% — that's 1,833 High-Risk customers.
- $155,849 in monthly recurring revenue sits in the High-Risk bucket.

**Critical distinction:** This score is a prioritization heuristic, NOT a predicted probability of churn. It tells us where to focus attention, not who will definitely leave.

**Transition:** "Now let's map specific actions to each segment."

---

## Slide 8: Segment-Specific Recommendations
**Estimated Duration: 90 seconds**

**Key Points:**
- **Priority 1 - Senior Vulnerable:** Dedicated senior support line (phone-first), 20% contract upgrade incentive, guided auto-pay migration, free security bundle, quarterly proactive calls. KPI: High-Risk % reduction, upgrade rate.
- **Priority 2 - Budget-Conscious:** "Essentials" value tier at ~$45/month, 15% annual discount, auto-pay credit campaign, usage alerts. Digital-first communication. KPI: Plan migration, auto-pay adoption.
- **Priority 3 - High-Value Long-Term:** Tiered loyalty program, 24-month price lock, dedicated account managers for top 20%, premium security and device upgrades, win-back protocol. Relationship-based communication. KPI: Revenue retention, NPS.
- **Priority 4 - New Vulnerable:** Structured 30/60/90 onboarding, default-on security (opt-out), first-year contract auto-convert at month 4, early warning system for support tickets. Digital-native messaging. KPI: 90-day retention, security adoption.

**Cross-segment quick wins** (immediate): Auto-pay migration, default-on security, risk score in CRM, monthly segment dashboards.

**Transition:** "What could this mean for the bottom line?"

---

## Slide 9: Expected Business Impact
**Estimated Duration: 75 seconds**

**Key Points:**
- Let me be clear: this is an **illustrative scenario**, not a forecast.
- If we achieve a 10% relative churn reduction among the 1,833 High-Risk customers — that's 183 customers retained.
- At an average of ~$85 monthly, that's ~$15,500 monthly or ~$186,000 annual revenue preserved.
- Total pilot investment: $750K across four segments. Illustrative Year-1 return: ~$2M — roughly 4x.
- **Assumptions:** 10% uplift only on High Risk (conservative), average revenue from monthly charges, no external factors modeled.
- **Caveats:** Requires A/B validation, not guaranteed, historical patterns ≠ future behavior.

**Transition:** "Before we invest, we need to acknowledge the limitations honestly."

---

## Slide 10: Implementation Roadmap & Limitations
**Estimated Duration: 75 seconds**

**Key Points:**
- **Immediate (Week 1-2):** CRM integration of risk scores, support team training on risk factors.
- **Month 1:** Automated daily scoring, segment dashboards, quick wins launch.
- **Quarter 1:** A/B test retention offers by segment, validate risk score against 90-day outcomes, calibrate thresholds.
- **Ongoing:** Quarterly refresh, scale winners, sunset losers.

**Limitations — I want to be transparent:**
1. Historical data doesn't guarantee future behavior — quarterly refresh is essential.
2. K-Means with Label Encoding has known sensitivity — we tested One-Hot separately.
3. Risk score is a heuristic, not a calibrated probability.
4. Segments are descriptive, not predictive.
5. No causal evidence — changing a factor may not reduce churn.
6. 75% overall churn is unusually high — validate on current production data.
7. Static snapshot — customer behavior evolves.
8. External factors (competitors, economy) not captured.
9. Illustrative impact scenarios require pilot validation.

**Transition:** "Let me close with three takeaways."

---

## Slide 11: Conclusion
**Estimated Duration: 45 seconds**

**Key Points:**
- **Takeaway 1:** Churn is pervasive at 75% but not uniform — four segments have distinct risk profiles requiring different actions.
- **Takeaway 2:** Transparent rule-based scoring enables immediate prioritization without black-box models — your teams can understand and trust it.
- **Takeaway 3:** Targeted pilots on High-Risk segments can demonstrate ROI before full-scale investment.

**Decision Requested:** Approve $750K pilot budget for 90-day segment-specific retention programs with A/B testing.

**Closing:** "Thank you. I'm happy to walk through any part in more detail and answer questions."

---

## Total Estimated Duration: ~10 minutes

**Rehearsal Notes:**
- Practice with a timer — aim for 9:30 to allow buffer
- Emphasize "illustrative," "heuristic," "historical" — never say "predicted" or "will"
- Have appendix slides ready for Q&A (methodology details, data quality, validation approach)
- Bring printed one-pager with segment table and roadmap for handout
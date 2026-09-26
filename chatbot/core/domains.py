# core/domains.py
from django.core.cache import cache
from api.models import Message

class BaseDomain:
    def __init__(self):
        self.name = "general"
        self.keywords = []
        self.max_context_messages = 5  # Default number of messages to remember
    
    def should_handle(self, text):
        """Check if this domain should handle the user input"""
        text = text.lower()
        return any(keyword in text for keyword in self.keywords)
    
    def generate_prompt(self, user_input, conversation=None):
        """
        Generate prompt with conversation context
        Args:
            user_input: Current user message
            conversation: Conversation object from models
        """
        history = self._get_conversation_history(conversation) if conversation else ""
        
        return f"""You are an AI assistant. Here's our conversation history:
        
{history}

Current Question: {user_input}

Please provide a helpful response:"""
    
    def process_output(self, output):
        """Process the raw output before sending to user"""
        return output
    
    def _get_conversation_history(self, conversation):
        """Retrieve and format conversation history"""
        messages = conversation.messages.all().order_by('-timestamp')[:self.max_context_messages]
        return "\n".join(
            f"User: {msg.user_message}\nAI: {msg.ai_response}" 
            for msg in reversed(messages)  # Show in chronological order
        )


class FinanceDomain(BaseDomain):
    def __init__(self):
        super().__init__()
        self.name = "finance"
        self.keywords = [
            'finance', 'financial', 'economy', 'economic', 'monetary', 'fiscal', 'capital', 'asset', 'liability', 'equity',
            'debt', 'investment', 'investing', 'portfolio', 'diversification', 'risk', 'return', 'yield', 'valuation',
            'liquidity', 'solvency', 'leverage', 'credit', 'interest', 'inflation', 'deflation', 'recession', 'depression',
            'growth', 'GDP', 'GNP', 'CPI', 'PPI', 'unemployment', 'employment', 'wages', 'income', 'expenditure', 'savings',
            'budget', 'surplus', 'deficit', 'tax', 'revenue', 'expenditure', 'subsidy', 'tariff', 'trade', 'balance of payments',
            'current account', 'capital account', 'foreign exchange', 'exchange rate', 'currency', 'devaluation', 'revaluation',
            'appreciation', 'depreciation', 'central bank', 'monetary policy', 'fiscal policy', 'interest rate', 'repo rate',
            'reverse repo rate', 'cash reserve ratio', 'statutory liquidity ratio', 'open market operations', 'quantitative easing',
            'quantitative tightening', 'inflation targeting', 'money supply', 'M1', 'M2', 'M3', 'M4', 'velocity of money',
            'financial market', 'money market', 'capital market', 'primary market', 'secondary market', 'stock market',
            'bond market', 'derivatives market', 'foreign exchange market', 'commodity market', 'real estate market',
            'mutual fund', 'exchange-traded fund', 'hedge fund', 'private equity', 'venture capital', 'angel investor',
            'initial public offering', 'follow-on public offering', 'rights issue', 'bonus issue', 'stock split', 'reverse stock split',
            'buyback', 'dividend', 'dividend yield', 'earnings per share', 'price-to-earnings ratio', 'price-to-book ratio',
            'price-to-sales ratio', 'price-to-cash flow ratio', 'market capitalization', 'enterprise value', 'book value',
            'net asset value', 'return on equity', 'return on assets', 'return on investment', 'return on capital employed',
            'debt-to-equity ratio', 'current ratio', 'quick ratio', 'cash ratio', 'interest coverage ratio', 'inventory turnover ratio',
            'asset turnover ratio', 'working capital', 'operating cycle', 'cash conversion cycle', 'free cash flow',
            'discounted cash flow', 'net present value', 'internal rate of return', 'payback period', 'profitability index',
            'capital budgeting', 'cost of capital', 'weighted average cost of capital', 'cost of equity', 'cost of debt',
            'beta', 'alpha', 'Sharpe ratio', 'Treynor ratio', 'Jensen s alpha', 'value at risk', 'expected shortfall',
            'stress testing', 'scenario analysis', 'sensitivity analysis', 'Monte Carlo simulation', 'black swan event',
            'systemic risk', 'idiosyncratic risk', 'market risk', 'credit risk', 'liquidity risk', 'operational risk',
            'regulatory risk', 'reputational risk', 'compliance risk', 'counterparty risk', 'default risk', 'interest rate risk',
            'exchange rate risk', 'commodity price risk', 'political risk', 'sovereign risk', 'legal risk', 'model risk',
            'cyber risk', 'environmental risk', 'social risk', 'governance risk', 'ESG', 'sustainable finance',
            'green finance', 'impact investing', 'socially responsible investing', 'ethical investing', 'carbon trading',
            'carbon credits', 'cap and trade', 'climate finance', 'climate risk', 'transition risk', 'physical risk',
            'stranded assets', 'green bonds', 'sustainability-linked bonds', 'social bonds', 'blue bonds', 'greenwashing',
            'financial inclusion', 'microfinance', 'financial literacy', 'digital finance', 'fintech', 'mobile banking',
            'internet banking', 'digital wallets', 'cryptocurrency', 'blockchain', 'bitcoin', 'ethereum', 'smart contracts',
            'decentralized finance', 'central bank digital currency', 'stablecoin', 'tokenization', 'initial coin offering',
            'security token offering', 'non-fungible token', 'digital assets', 'digital identity', 'know your customer',
            'anti-money laundering', 'combating the financing of terrorism', 'financial regulation', 'financial supervision',
            'financial stability', 'systemically important financial institution', 'too big to fail', 'living will',
            'resolution planning', 'bail-in', 'bail-out', 'deposit insurance', 'lender of last resort', 'moral hazard',
            'regulatory arbitrage', 'shadow banking', 'financial innovation', 'financial engineering', 'structured finance',
            'securitization', 'mortgage-backed securities', 'asset-backed securities', 'collateralized debt obligations',
            'credit default swaps', 'interest rate swaps', 'currency swaps', 'futures', 'options', 'forwards', 'derivatives',
            'hedging', 'speculation', 'arbitrage', 'short selling', 'margin trading', 'leverage', 'stop loss', 'limit order',
            'market order', 'order book', 'bid-ask spread', 'liquidity', 'volatility', 'beta', 'alpha', 'Sharpe ratio',
            'technical analysis', 'fundamental analysis', 'chart patterns', 'candlestick patterns', 'moving averages',
            'relative strength index', 'MACD', 'Bollinger Bands', 'Fibonacci retracement', 'Elliott Wave Theory',
            'Dow Theory', 'support and resistance', 'trend lines', 'volume analysis', 'momentum indicators', 'oscillators',
            'mean reversion', 'breakout', 'pullback', 'consolidation', 'divergence', 'overbought', 'oversold',
            'bull market', 'bear market', 'market correction', 'market crash', 'market rally', 'market bubble',
            'market sentiment', 'investor psychology', 'behavioral finance', 'herd behavior', 'loss aversion',
            'anchoring bias', 'confirmation bias', 'overconfidence', 'representativeness heuristic', 'availability heuristic',
            'mental accounting', 'prospect theory', 'efficient market hypothesis', 'random walk theory', 'capital asset pricing model',
            'arbitrage pricing theory', 'Fama-French three-factor model', 'Carhart four-factor model', 'multi-factor models',
            'quantitative investing', 'algorithmic trading', 'high-frequency trading', 'robo-advisors', 'passive investing',
            'active investing', 'index funds', 'exchange-traded funds', 'smart beta', 'factor investing', 'value investing',
            'growth investing', 'momentum investing', 'income investing', 'dividend investing', 'small-cap investing',
            'large-cap investing', 'international investing', 'emerging markets', 'frontier markets', 'developed markets',
            'market capitalization', 'free float', 'float-adjusted market cap', 'equal-weighted index', 'market-weighted index',
            'price-weighted index', 'total return index', 'benchmark', 'tracking error', 'information ratio', 'active share',
            'style box', 'style drift', 'style investing', 'sector rotation', 'top-down approach', 'bottom-up approach',
            'macro investing', 'micro investing', 'thematic investing', 'event-driven investing', 'merger arbitrage',
            'distressed investing', 'special situations', 'long/short equity', 'market neutral', 'statistical arbitrage',
            'pair trading', 'convertible arbitrage', 'fixed income arbitrage', 'global macro', 'managed futures',
            'commodity trading advisors', 'fund of funds', 'multi-strategy funds', 'absolute return', 'relative return',
            'alpha generation', 'beta exposure', 'risk-adjusted return', 'performance attribution', 'style analysis',
            'peer group analysis', 'benchmarking', 'performance measurement', 'performance evaluation', 'performance reporting',
            'compliance', 'regulatory reporting', 'risk management', 'portfolio construction', 'asset allocation',
            'strategic asset allocation', 'tactical asset allocation', 'dynamic asset allocation', 'liability-driven investing',
            'goals-based investing', 'target-date funds', 'lifecycle funds', 'glide path', 'rebalancing', 'drift',
            'tax efficiency', 'tax loss harvesting', 'wash sale rule', 'capital gains', 'capital losses', 'dividends',
            'interest income', 'qualified dividends', 'non-qualified dividends', 'ordinary income', 'tax-deferred',
            'tax-exempt', 'taxable account', 'tax-advantaged account', 'individual retirement account', 'Roth IRA',
            '401(k)', '403(b)', '457(b)', 'pension plan', 'defined benefit plan', 'defined contribution plan',
            'annuities', 'life insurance', 'health insurance', 'disability insurance', 'long-term care insurance',
            'property insurance', 'casualty insurance', 'liability insurance', 'umbrella insurance', 'reinsurance',
            'underwriting', 'actuarial science', 'premium', 'deductible', 'copayment', 'coinsurance', 'out-of-pocket maximum',
            'policyholder', 'beneficiary', 'claim', 'loss ratio', 'combined ratio', 'reserve', 'surplus', 'solvency',
            'risk-based capital', 'rating agencies', 'credit rating', 'investment grade', 'junk bond', 'default',
            'credit spread', 'yield curve', 'term structure', 'duration', 'convexity', 'interest rate risk',
            'call risk', 'prepayment risk', 'extension risk', 'reinvestment risk', 'inflation risk', 'liquidity risk',
            'credit risk', 'default risk', 'sovereign risk', 'political risk', 'currency risk', 'market risk',
            'systemic risk', 'idiosyncratic risk', 'operational risk', 'legal risk', 'regulatory risk', 'reputational risk',
            'model','nifty', 'nifty 50', 'stock market', 'stock index', 'index calculation', 'sensex', 
'bse', 'nse', 'market index', 'equity index', 'index fund']


        self.max_context_messages = 6  # Remember more context for financial discussions
    
    def generate_prompt(self, user_input, conversation=None):
        base_prompt = super().generate_prompt(user_input, conversation)
        return f"""As a certified financial analyst, provide professional analysis considering:
        
1. Any previously discussed financial instruments
2. Current market conditions
3. Relevant financial metrics

Guidelines:
- Mention P/E ratio, 52-week range, and dividend yield when appropriate
- Compare to sector benchmarks
- Highlight both risks and opportunities

{base_prompt}"""
    
    def process_output(self, output):
        disclaimer = (
            "\n\n* <h4>Disclaimer: This analysis is for informational purposes only. "
            "Not financial advice. Past performance ≠ future results. "
            "Consult a qualified financial advisor before making investment decisions.*"
        )
        return f"{output}{disclaimer}"


class HealthcareDomain(BaseDomain):
    def __init__(self):
        super().__init__()
        self.name = "healthcare"
        self.keywords = [
    'health', 'healthcare', 'wellness', 'fitness', 'nutrition', 'exercise', 'diet', 'obesity', 'weight loss', 'BMI',
            'mental health', 'stress', 'anxiety', 'depression', 'therapy', 'counseling', 'psychology', 'psychiatry',
            'addiction', 'rehabilitation', 'recovery', 'substance abuse', 'alcoholism', 'smoking cessation','vitamin D',
            # Medical Professionals
            'doctor', 'physician', 'nurse', 'surgeon', 'therapist', 'psychiatrist', 'psychologist', 'pediatrician',
            'cardiologist', 'neurologist', 'dermatologist', 'endocrinologist', 'gastroenterologist', 'oncologist',
            'radiologist', 'anesthesiologist', 'urologist', 'gynecologist', 'obstetrician', 'orthopedist', 'ophthalmologist',
            # Medical Facilities
            'hospital', 'clinic', 'emergency room', 'ICU', 'operating room', 'pharmacy', 'laboratory', 'rehabilitation center',
            'nursing home', 'urgent care', 'primary care', 'specialty clinic', 'mental health facility',
            # Medical Procedures
            'surgery', 'biopsy', 'endoscopy', 'colonoscopy', 'chemotherapy', 'radiation therapy', 'dialysis', 'transplant',
            'vaccination', 'immunization', 'physical therapy', 'occupational therapy', 'speech therapy', 'counseling',
            'psychotherapy', 'diagnostic imaging', 'MRI', 'CT scan', 'X-ray', 'ultrasound', 'PET scan',
            # Medical Conditions
            'diabetes', 'hypertension', 'asthma', 'COPD', 'arthritis', 'osteoporosis', 'cancer', 'stroke', 'heart disease',
            'Alzheimer\'s disease', 'Parkinson\'s disease', 'epilepsy', 'multiple sclerosis', 'HIV/AIDS', 'hepatitis',
            'influenza', 'pneumonia', 'tuberculosis', 'COVID-19', 'malaria', 'dengue', 'cholera', 'obesity',
            # Symptoms
            'fever', 'cough', 'headache', 'nausea', 'vomiting', 'diarrhea', 'fatigue', 'dizziness', 'shortness of breath',
            'chest pain', 'abdominal pain', 'back pain', 'joint pain', 'muscle pain', 'rash', 'itching', 'swelling',
            'bleeding', 'numbness', 'tingling', 'insomnia', 'anxiety', 'depression',
            # Medications
            'antibiotics', 'analgesics', 'antipyretics', 'antidepressants', 'antihypertensives', 'insulin', 'vaccines',
            'chemotherapy drugs', 'antivirals', 'antifungals', 'steroids', 'immunosuppressants', 'antacids',
            'antihistamines', 'bronchodilators', 'diuretics', 'laxatives', 'sedatives', 'anesthetics',
            # Medical Equipment
            'stethoscope', 'thermometer', 'blood pressure monitor', 'glucometer', 'pulse oximeter', 'ECG machine',
            'defibrillator', 'ventilator', 'syringe', 'scalpel', 'forceps', 'IV drip', 'catheter', 'wheelchair',
            'hospital bed', 'oxygen tank', 'nebulizer', 'dialysis machine', 'X-ray machine', 'MRI machine',
            # Health Insurance
            'health insurance', 'medical insurance', 'premium', 'deductible', 'co-pay', 'coverage', 'policy',
            'claim', 'network', 'preauthorization', 'Medicare', 'Medicaid', 'private insurance', 'public health insurance',
            # Public Health
            'epidemic', 'pandemic', 'quarantine', 'isolation', 'contact tracing', 'vaccination campaign',
            'public health policy', 'health education', 'disease prevention', 'sanitation', 'water purification',
            'vector control', 'nutrition programs', 'maternal health', 'child health', 'immunization schedule',
            # Medical Research
            'clinical trial', 'placebo', 'double-blind study', 'randomized controlled trial', 'informed consent',
            'ethics committee', 'institutional review board', 'medical journal', 'peer review', 'case study',
            'meta-analysis', 'systematic review', 'evidence-based medicine', 'translational research',
            # Health Technology
            'telemedicine', 'telehealth', 'electronic health record', 'health information system', 'medical app',
            'wearable device', 'fitness tracker', 'remote monitoring', 'health data analytics', 'AI in healthcare',
            'robotic surgery', '3D printing in medicine', 'virtual reality therapy', 'mobile health',
            # Health and Wellness
            'balanced diet', 'nutritional supplements', 'hydration', 'physical activity', 'sleep hygiene',
            'stress management', 'mindfulness', 'yoga', 'meditation', 'preventive care', 'screening tests',
            'health check-up', 'vaccination', 'smoking cessation', 'alcohol moderation',
            # Emergency Care
            'first aid', 'CPR', 'emergency response', 'ambulance', 'paramedic', 'trauma care', 'burn treatment',
            'poison control', 'disaster response', 'emergency preparedness',
            # Miscellaneous
            'medical ethics', 'patient rights', 'informed consent', 'advance directive', 'organ donation',
            'medical malpractice', 'healthcare policy', 'healthcare reform', 'universal healthcare',
            'healthcare access', 'healthcare disparities', 'healthcare quality', 'patient safety',
            # Additional Keywords
            'genetic counseling', 'gene therapy', 'stem cell therapy', 'personalized medicine', 'pharmacogenomics',
            'biomarker', 'precision medicine', 'nanomedicine', 'biotechnology', 'regenerative medicine',
            'clinical guidelines', 'standard of care', 'medical coding', 'ICD codes', 'CPT codes',
            'healthcare accreditation', 'Joint Commission', 'patient satisfaction', 'healthcare analytics',
            'population health', 'value-based care', 'accountable care organization', 'care coordination',
            'chronic disease management', 'patient engagement', 'health literacy', 'caregiver support',
            'home healthcare', 'palliative care', 'hospice care', 'end-of-life care', 'advance care planning',
            'medical tourism', 'global health', 'travel medicine', 'occupational health', 'environmental health',
            'school health', 'workplace wellness', 'community health', 'epidemiology', 'biostatistics',
            'health economics', 'healthcare financing', 'healthcare marketing', 'healthcare administration',
            'healthcare management', 'healthcare leadership', 'healthcare innovation', 'healthcare entrepreneurship',
            'healthcare startups', 'digital health', 'health informatics', 'clinical informatics',
            'public health informatics', 'healthcare interoperability', 'FHIR', 'HL7', 'healthcare cybersecurity',
            'patient portal', 'health information exchange', 'medical billing', 'revenue cycle management',
            'utilization management', 'case management', 'disease registry', 'quality improvement',
            'performance metrics', 'benchmarking', 'clinical decision support', 'e-prescribing',
            'medication reconciliation', 'adverse event reporting', 'pharmacovigilance', 'drug safety',
            'medication adherence', 'polypharmacy', 'medication therapy management', 'formulary management',
            'drug formulary', 'prior authorization', 'step therapy', 'medication error', 'drug interaction',
            'black box warning', 'off-label use', 'compounding pharmacy', 'specialty pharmacy',
            'mail-order pharmacy', 'pharmacy benefit manager', 'prescription drug plan', 'medication discount',
            'patient assistance program', 'co-pay card', 'drug coupon', 'generic drug', 'brand-name drug',
            'biosimilar', 'biologic', 'orphan drug', 'rare disease', 'clinical pathway', 'care protocol',
            'evidence-based guideline', 'clinical algorithm', 'best practice', 'standard operating procedure',
            'clinical audit', 'root cause analysis', 'failure mode and effects analysis', 'incident reporting',
            'patient safety culture', 'just culture', 'safety huddle', 'safety checklist', 'hand hygiene',
            'infection control', 'antimicrobial stewardship', 'isolation precautions', 'personal protective equipment',
            'needle stick injury', 'sharps disposal', 'medical waste management', 'environmental cleaning',
            'airborne precautions', 'droplet precautions', 'contact precautions', 'negative pressure room',
            'sterilization', 'disinfection', 'aseptic technique', 'surgical site infection', 'catheter-associated infection',
            'ventilator-associated pneumonia', 'central line-associated bloodstream infection', 'hospital-acquired infection',
            'nosocomial infection', 'multidrug-resistant organism', 'MRSA', 'VRE', 'C. difficile', 'infection surveillance',
            'outbreak investigation', 'epidemic curve', 'case definition', 'index case', 'contact tracing',
            'quarantine', 'isolation', 'public health emergency', 'pandemic preparedness', 'emergency operations center',
            'incident command system', 'mass casualty incident', 'bioterrorism', 'chemical exposure', 'radiation exposure',
            'hazardous materials', 'personal protective equipment', 'decontamination', 'emergency drills',
            'surge capacity', 'triage', 'disaster response', 'community resilience', 'risk communication',
            'health communication', 'health promotion', 'behavior change', 'social determinants of health',
            'health equity', 'health disparity', 'vulnerable populations', 'underserved communities',
            'cultural competence', 'language access', 'health navigator', 'community health worker',
            'peer support', 'patient advocacy', 'shared decision-making', 'informed consent', 'health coaching',
            'motivational interviewing', 'self-management','virus and a bacterium', 'bacteria', 'virus', 'fungus','allergic', 'parasite',
]

        self.max_context_messages = 4  # Medical context needs less history
    
    def generate_prompt(self, user_input, conversation=None):
        base_prompt = super().generate_prompt(user_input, conversation)
        return f"""As a licensed healthcare professional, provide general medical information.

Important Considerations:
1. Any symptoms mentioned previously
2. Context from earlier questions
3. General wellness information

Rules:
- Never diagnose specific conditions
- For serious symptoms, recommend immediate professional care
- Only suggest general OTC medication information
- Highlight red flag symptoms

{base_prompt}"""
    
    def process_output(self, output):
        warning = (
            "\n\n* <h4> Important: This is not medical advice. "
            "For proper diagnosis and treatment, please consult a qualified healthcare provider. "
            "In emergencies, call your local emergency number immediately.*"
        )
        return f"{output}{warning}"


def get_domain_handler(user_input):
    """Factory function to get the appropriate domain handler"""
    domains = [FinanceDomain(), HealthcareDomain()]
    for domain in domains:
        if domain.should_handle(user_input):
            return domain
    return BaseDomain()
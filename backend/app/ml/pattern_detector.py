"""
Pattern Detection System
Detects potentially unfair or illegal clauses in legal documents
"""
import re
from typing import List, Dict


class PatternDetector:
    """Detect unfair clauses and violations in legal documents"""
    
    def __init__(self):
        self.patterns = self._load_patterns()
    
    def _load_patterns(self):
        """Load pattern rules for detecting unfair clauses"""
        return {
            'unfair_repairs': {
                'patterns': [
                    r'tenant.*responsible.*all.*repair',
                    r'tenant.*maintain.*structure',
                    r'tenant.*fix.*structural.*damage',
                    r'no.*landlord.*responsibility.*repair',
                    r'tenant.*liable.*for.*all.*maintenance'
                ],
                'severity': 'HIGH',
                'explanation': 'Landlord is legally responsible for structural repairs, plumbing, heating, and electrical systems',
                'legal_ref': 'Landlord and Tenant Act 1985 Section 11'
            },
            'unfair_deposit': {
                'patterns': [
                    r'non-refundable.*deposit',
                    r'deposit.*not.*return',
                    r'deposit.*exceed.*\d+.*week',
                    r'deposit.*not.*protect',
                    r'deposit.*£\d{4,}',  # Likely excessive
                    r'deposit.*\d+.*month.*rent'
                ],
                'severity': 'CRITICAL',
                'explanation': 'Deposit must be refundable, protected in government scheme, and not exceed 5 weeks rent',
                'legal_ref': 'Housing Act 2004, Tenant Fees Act 2019'
            },
            'illegal_fees': {
                'patterns': [
                    r'administration.*fee',
                    r'reference.*check.*fee',
                    r'viewing.*fee',
                    r'renewal.*fee',
                    r'check-in.*fee',
                    r'check-out.*fee',
                    r'inventory.*fee'
                ],
                'severity': 'HIGH',
                'explanation': 'Most fees to tenants are prohibited under the Tenant Fees Act 2019',
                'legal_ref': 'Tenant Fees Act 2019'
            },
            'unfair_access': {
                'patterns': [
                    r'landlord.*enter.*anytime',
                    r'no.*notice.*require.*inspection',
                    r'tenant.*must.*allow.*access.*immediately',
                    r'landlord.*may.*enter.*without.*permission'
                ],
                'severity': 'MEDIUM',
                'explanation': 'Landlord must give 24 hours notice before entering property except in emergencies',
                'legal_ref': 'Protection from Eviction Act 1977'
            },
            'invalid_eviction': {
                'patterns': [
                    r'section 21.*notice',
                    r'evict.*without.*court.*order',
                    r'leave.*immediately',
                    r'24.*hour.*eviction',
                    r'no-fault.*eviction',
                    r'must.*vacate.*\d+.*day'
                ],
                'severity': 'CRITICAL',
                'explanation': 'Section 21 no-fault evictions were abolished in October 2025. Proper legal process must be followed',
                'legal_ref': 'Renters Rights Act 2025'
            },
            'unfair_rent_increase': {
                'patterns': [
                    r'rent.*increase.*at.*landlord.*discretion',
                    r'rent.*may.*increase.*without.*notice',
                    r'unlimited.*rent.*increase',
                    r'rent.*increase.*\d+%.*per.*year'
                ],
                'severity': 'MEDIUM',
                'explanation': 'Rent increases must be fair and follow proper procedures. Tenants can challenge excessive increases',
                'legal_ref': 'Housing Act 1988'
            },
            'prohibited_restrictions': {
                'patterns': [
                    r'no.*visitors.*allowed',
                    r'no.*guests.*overnight',
                    r'tenant.*cannot.*have.*visitors',
                    r'blanket.*pet.*ban'
                ],
                'severity': 'MEDIUM',
                'explanation': 'Unreasonable restrictions on quiet enjoyment may be unenforceable',
                'legal_ref': 'Common Law - Quiet Enjoyment'
            },
            'retaliatory_clauses': {
                'patterns': [
                    r'cannot.*report.*repair',
                    r'penalty.*for.*complaint',
                    r'eviction.*if.*report',
                    r'fine.*for.*contacting.*council'
                ],
                'severity': 'CRITICAL',
                'explanation': 'Retaliatory eviction for reporting repairs is illegal',
                'legal_ref': 'Deregulation Act 2015'
            }
        }
    
    def detect(self, text: str) -> List[Dict]:
        """
        Detect problematic patterns in document text
        
        Args:
            text: Document text to analyze
            
        Returns:
            List of detected issues with details
        """
        detected_issues = []
        text_lower = text.lower()
        
        for issue_type, config in self.patterns.items():
            for pattern in config['patterns']:
                matches = re.finditer(pattern, text_lower, re.IGNORECASE)
                
                for match in matches:
                    # Get context around match
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end]
                    
                    detected_issues.append({
                        'issue': issue_type,
                        'severity': config['severity'],
                        'matched_text': match.group(0),
                        'context': context,
                        'position': match.span(),
                        'explanation': config['explanation'],
                        'legal_reference': config['legal_ref'],
                        'recommendations': self._get_recommendations(issue_type)
                    })
        
        return detected_issues
    
    def _get_recommendations(self, issue_type: str) -> List[str]:
        """Generate recommendations based on detected issue"""
        recommendations = {
            'unfair_repairs': [
                'Landlord must maintain structure, exterior, and installations',
                'Request written clarification of repair responsibilities',
                'Contact local council housing team if repairs not done',
                'Keep records of all repair requests and responses'
            ],
            'unfair_deposit': [
                'Ensure deposit is protected in government-approved scheme',
                'Maximum deposit is 5 weeks rent (or 6 weeks if annual rent over £50,000)',
                'Request deposit protection certificate within 30 days',
                'Contact Shelter or Citizens Advice for support'
            ],
            'illegal_fees': [
                'Request immediate refund of prohibited fees',
                'Report to Trading Standards if fees not returned',
                'Landlord/agent faces fines: £5,000 (first offense), £30,000 (repeat)',
                'Keep evidence of all payments made'
            ],
            'unfair_access': [
                'Landlord must give 24 hours notice except emergencies',
                'You have right to refuse entry without proper notice',
                'Document all entry attempts and communications',
                'Contact police if landlord enters without permission'
            ],
            'invalid_eviction': [
                'Section 21 no-fault evictions are no longer legal (abolished Oct 2025)',
                'Continue paying rent and remain in property',
                'Any eviction must follow proper legal process with court order',
                'Call police (999) if landlord attempts illegal eviction',
                'Contact Shelter or Citizens Advice immediately'
            ],
            'unfair_rent_increase': [
                'Rent increases must follow terms in tenancy agreement',
                'Can challenge excessive increases at tribunal',
                'Landlord must give proper notice (usually 1 month)',
                'Keep evidence of local rental prices for comparison'
            ],
            'prohibited_restrictions': [
                'Unreasonable restrictions may be unenforceable',
                'Right to quiet enjoyment of property',
                'Blanket pet bans can be challenged (Renters Rights Act 2025)',
                'Seek legal advice if restrictions are excessive'
            ],
            'retaliatory_clauses': [
                'Retaliatory eviction for reporting repairs is illegal',
                'Protected for 6 months after reporting to council',
                'Document all repair requests and responses',
                'Contact Shelter if facing retaliation'
            ]
        }
        
        return recommendations.get(issue_type, [
            'Seek legal advice from Shelter or Citizens Advice',
            'Document all communications with landlord',
            'Know your rights under UK housing law'
        ])
    
    def analyze_severity(self, issues: List[Dict]) -> Dict:
        """Analyze overall severity of detected issues"""
        if not issues:
            return {
                'overall_risk': 'LOW',
                'critical_count': 0,
                'high_count': 0,
                'medium_count': 0,
                'summary': 'No significant issues detected'
            }
        
        critical = sum(1 for i in issues if i['severity'] == 'CRITICAL')
        high = sum(1 for i in issues if i['severity'] == 'HIGH')
        medium = sum(1 for i in issues if i['severity'] == 'MEDIUM')
        
        if critical > 0:
            overall_risk = 'CRITICAL'
            summary = f'{critical} critical issue(s) detected. Seek legal advice immediately.'
        elif high > 0:
            overall_risk = 'HIGH'
            summary = f'{high} high-priority issue(s) detected. Review carefully and seek advice.'
        else:
            overall_risk = 'MEDIUM'
            summary = f'{medium} issue(s) detected. Review and consider seeking advice.'
        
        return {
            'overall_risk': overall_risk,
            'critical_count': critical,
            'high_count': high,
            'medium_count': medium,
            'total_issues': len(issues),
            'summary': summary
        }

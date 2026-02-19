"""
Graceful Degradation Handler
Provides multi-tier fallback strategies for document analysis
"""
import re
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class GracefulDegradationHandler:
    """
    Handle service failures with fallback strategies
    
    Tier 1: Full ML pipeline (OCR + Classification + Pattern Detection)
    Tier 2: Rule-based extraction only
    Tier 3: Basic text analysis
    """
    
    def analyze_document_with_fallback(
        self,
        document_id: str,
        extracted_text: str,
        file_type: str
    ) -> Dict:
        """
        Multi-tier fallback strategy for document analysis
        
        Args:
            document_id: Unique document identifier
            extracted_text: OCR extracted text
            file_type: Document file type
            
        Returns:
            Analysis result with tier indicator
        """
        try:
            # Tier 1: Full ML pipeline
            logger.info(
                f"Attempting Tier 1 (Full ML) analysis",
                extra={'document_id': document_id}
            )
            return self._full_ml_analysis(document_id, extracted_text, file_type)
            
        except Exception as e:
            logger.warning(
                f"Tier 1 ML pipeline failed: {str(e)}. "
                f"Falling back to Tier 2 (Rule-based)",
                extra={'document_id': document_id}
            )
            
            try:
                # Tier 2: Rule-based extraction
                return self._rule_based_analysis(document_id, extracted_text)
                
            except Exception as e:
                logger.error(
                    f"Tier 2 rule-based analysis failed: {str(e)}. "
                    f"Using Tier 3 (Basic)",
                    extra={'document_id': document_id}
                )
                
                # Tier 3: Basic text analysis (always works)
                return self._basic_text_analysis(document_id, extracted_text)
    
    def _full_ml_analysis(
        self,
        document_id: str,
        text: str,
        file_type: str
    ) -> Dict:
        """
        Complete ML-based analysis using all models
        
        This would use:
        - Document classifier for type detection
        - Pattern detector for issue identification
        - Entity extraction for structured data
        """
        from app.services.ml_service import MLService
        
        # Use ML service for classification and pattern detection
        classification = MLService.classify_document(text)
        detected_issues = MLService.detect_patterns(text)  # This returns a list
        
        # Analyze severity
        severity_analysis = MLService.analyze_severity(detected_issues)
        
        # Generate summary
        summary = self._generate_ml_summary(text, classification, detected_issues)
        
        return {
            'analysis_tier': 'FULL_ML',
            'confidence': 'HIGH',
            'classification': classification,
            'detected_issues': detected_issues,
            'severity_analysis': severity_analysis,
            'summary': summary,
            'recommendations': self._generate_recommendations_ml(detected_issues),
            'warning': None
        }
    
    def _generate_ml_summary(self, text: str, classification: Dict, issues: List) -> str:
        """Generate summary from ML analysis"""
        doc_type = classification.get('category', 'Unknown')
        confidence = classification.get('confidence', 0)
        issue_count = len(issues)
        
        if issue_count == 0:
            return f"This appears to be a {doc_type} (confidence: {confidence:.0%}). No significant issues detected."
        else:
            high_severity = sum(1 for i in issues if i.get('severity') == 'HIGH')
            if high_severity > 0:
                return f"This {doc_type} has {issue_count} potential issues, including {high_severity} high-severity concerns that require immediate attention."
            else:
                return f"This {doc_type} has {issue_count} potential issues that should be reviewed."
    
    def _generate_recommendations_ml(self, issues: List) -> List[str]:
        """Generate recommendations from ML-detected issues"""
        recommendations = []
        
        for issue in issues:
            severity = issue.get('severity', 'MEDIUM')
            issue_type = issue.get('issue_type', 'Unknown issue')
            
            if severity == 'HIGH':
                recommendations.append(f"⚠️ Address {issue_type} immediately - this is a high-priority concern")
            elif severity == 'MEDIUM':
                recommendations.append(f"Review {issue_type} with a legal professional")
        
        if not recommendations:
            recommendations.append("Document appears compliant, but consider professional review for peace of mind")
        
        return recommendations
    
    def _rule_based_analysis(self, document_id: str, text: str) -> Dict:
        """
        Regex and rule-based extraction
        
        Uses pattern matching for:
        - Entity extraction (names, amounts, dates)
        - Risk detection (keywords, phrases)
        - Document classification (keywords)
        """
        logger.info(
            "Using rule-based analysis",
            extra={'document_id': document_id}
        )
        
        # Extract entities using regex
        entities = {
            'tenant_name': self._extract_tenant_regex(text),
            'landlord_name': self._extract_landlord_regex(text),
            'rent_amount': self._extract_rent_regex(text),
            'deposit_amount': self._extract_deposit_regex(text),
            'dates': self._extract_dates_regex(text),
            'property_address': self._extract_address_regex(text)
        }
        
        # Classify document type
        doc_type = self._classify_document_regex(text)
        
        # Detect risks using keywords
        risks = self._detect_risks_regex(text)
        
        # Calculate severity
        severity_analysis = self._calculate_severity_regex(risks)
        
        # Generate summary
        summary = self._generate_rule_based_summary(doc_type, risks, severity_analysis)
        
        return {
            'analysis_tier': 'RULE_BASED',
            'confidence': 'MEDIUM',
            'classification': {
                'category': doc_type,
                'confidence': 0.7
            },
            'detected_issues': risks,
            'severity_analysis': severity_analysis,
            'summary': summary,
            'recommendations': self._generate_recommendations_regex(risks),
            'warning': 'ML models unavailable. Using pattern matching. Results may be less accurate.'
        }
    
    def _generate_rule_based_summary(self, doc_type: str, risks: List[Dict], severity: Dict) -> str:
        """Generate summary for rule-based analysis"""
        issue_count = len(risks)
        overall_risk = severity.get('overall_risk', 'LOW')
        
        if issue_count == 0:
            return f"This appears to be a {doc_type.replace('_', ' ').title()}. No significant issues detected using pattern matching."
        else:
            critical = severity.get('critical_count', 0)
            high = severity.get('high_count', 0)
            
            if critical > 0:
                return f"This {doc_type.replace('_', ' ').title()} has {issue_count} potential issues detected, including {critical} critical concerns that require immediate attention."
            elif high > 0:
                return f"This {doc_type.replace('_', ' ').title()} has {issue_count} potential issues detected, including {high} high-priority concerns that should be reviewed carefully."
            else:
                return f"This {doc_type.replace('_', ' ').title()} has {issue_count} potential issues that should be reviewed."
    
    def _basic_text_analysis(self, document_id: str, text: str) -> Dict:
        """
        Minimal analysis when all else fails
        
        Provides basic statistics and warnings
        """
        logger.warning(
            "Using basic text analysis only",
            extra={'document_id': document_id}
        )
        
        word_count = len(text.split())
        char_count = len(text)
        
        # Basic keyword detection
        has_tenancy = 'tenancy' in text.lower() or 'lease' in text.lower()
        has_rent = 'rent' in text.lower()
        has_deposit = 'deposit' in text.lower()
        
        return {
            'analysis_tier': 'BASIC',
            'confidence': 'LOW',
            'classification': {
                'document_type': 'TENANCY_AGREEMENT' if has_tenancy else 'UNKNOWN',
                'confidence': 0.3
            },
            'detected_issues': [],
            'severity_analysis': {
                'overall_risk': 'UNKNOWN',
                'risk_score': 0
            },
            'statistics': {
                'word_count': word_count,
                'char_count': char_count,
                'has_tenancy_keywords': has_tenancy,
                'has_rent_keywords': has_rent,
                'has_deposit_keywords': has_deposit
            },
            'warning': 'Limited analysis available. Manual review strongly recommended.'
        }
    
    # Regex-based extraction methods
    
    def _extract_tenant_regex(self, text: str) -> List[str]:
        """Extract tenant names using regex patterns"""
        patterns = [
            r'tenant[:\s]+([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'the tenant,?\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
        ]
        
        names = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            names.extend(matches)
        
        return list(set(names))[:3]  # Return up to 3 unique names
    
    def _extract_landlord_regex(self, text: str) -> List[str]:
        """Extract landlord names using regex patterns"""
        patterns = [
            r'landlord[:\s]+([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'the landlord,?\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
        ]
        
        names = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            names.extend(matches)
        
        return list(set(names))[:3]
    
    def _extract_rent_regex(self, text: str) -> List[str]:
        """Extract rent amounts using regex patterns"""
        patterns = [
            r'£\s*(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:per month|pcm|monthly)',
            r'rent[:\s]+£\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
        ]
        
        amounts = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            amounts.extend([f"£{m}" for m in matches])
        
        return list(set(amounts))[:3]
    
    def _extract_deposit_regex(self, text: str) -> List[str]:
        """Extract deposit amounts using regex patterns"""
        patterns = [
            r'deposit[:\s]+£\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
            r'security deposit[:\s]+£\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
        ]
        
        amounts = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            amounts.extend([f"£{m}" for m in matches])
        
        return list(set(amounts))[:3]
    
    def _extract_dates_regex(self, text: str) -> List[str]:
        """Extract dates using regex patterns"""
        patterns = [
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',
            r'\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}',
        ]
        
        dates = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)
        
        return list(set(dates))[:5]
    
    def _extract_address_regex(self, text: str) -> List[str]:
        """Extract property addresses using regex patterns"""
        # Simple pattern for UK addresses
        pattern = r'\d+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*'
        
        addresses = re.findall(pattern, text)
        return list(set(addresses))[:2]
    
    def _classify_document_regex(self, text: str) -> str:
        """Classify document type using keyword matching"""
        text_lower = text.lower()
        
        if 'tenancy agreement' in text_lower or 'assured shorthold' in text_lower:
            return 'TENANCY_AGREEMENT'
        elif 'gas safety' in text_lower:
            return 'GAS_SAFETY_CERTIFICATE'
        elif 'energy performance' in text_lower or 'epc' in text_lower:
            return 'EPC_CERTIFICATE'
        elif 'deposit protection' in text_lower:
            return 'DEPOSIT_PROTECTION'
        else:
            return 'OTHER'
    
    def _detect_risks_regex(self, text: str) -> List[Dict]:
        """Detect potential risks using keyword matching"""
        risks = []
        text_lower = text.lower()
        
        # Check for missing deposit scheme mention
        if 'deposit' in text_lower and 'protection' not in text_lower and 'scheme' not in text_lower:
            risks.append({
                'issue': 'missing_deposit_scheme',
                'severity': 'HIGH',
                'matched_text': 'deposit mentioned without protection scheme',
                'explanation': 'No mention of deposit protection scheme. UK law requires deposits to be protected within 30 days.',
                'recommendations': [
                    'Ensure deposit is protected in government-approved scheme',
                    'Request deposit protection certificate within 30 days',
                    'Contact Shelter or Citizens Advice for support'
                ]
            })
        
        # Check for excessive fees
        if any(word in text_lower for word in ['fee', 'charge', 'payment']) and 'tenant' in text_lower:
            risks.append({
                'issue': 'potential_fees',
                'severity': 'MEDIUM',
                'matched_text': 'fees or charges mentioned',
                'explanation': 'Document mentions fees or charges. Most fees to tenants are prohibited under the Tenant Fees Act 2019.',
                'recommendations': [
                    'Request immediate refund of prohibited fees',
                    'Report to Trading Standards if fees not returned',
                    'Keep evidence of all payments made'
                ]
            })
        
        # Check for unclear notice period
        if 'notice' in text_lower and 'period' not in text_lower:
            risks.append({
                'issue': 'unclear_notice_period',
                'severity': 'MEDIUM',
                'matched_text': 'notice mentioned without clear period',
                'explanation': 'Notice requirements may be unclear. Proper notice periods must be specified.',
                'recommendations': [
                    'Clarify the notice period requirements with your landlord in writing',
                    'Ensure notice periods comply with legal minimums',
                    'Keep records of all notice communications'
                ]
            })
        
        # Check for repair responsibilities
        if 'tenant' in text_lower and 'repair' in text_lower and 'responsible' in text_lower:
            risks.append({
                'issue': 'unfair_repairs',
                'severity': 'HIGH',
                'matched_text': 'tenant repair responsibilities mentioned',
                'explanation': 'Landlord is legally responsible for structural repairs, plumbing, heating, and electrical systems.',
                'recommendations': [
                    'Landlord must maintain structure, exterior, and installations',
                    'Request written clarification of repair responsibilities',
                    'Contact local council housing team if repairs not done'
                ]
            })
        
        return risks
    
    def _calculate_severity_regex(self, risks: List[Dict]) -> Dict:
        """Calculate overall severity from detected risks"""
        if not risks:
            return {
                'overall_risk': 'LOW',
                'critical_count': 0,
                'high_count': 0,
                'medium_count': 0,
                'total_issues': 0,
                'summary': 'No significant issues detected'
            }
        
        critical_count = sum(1 for r in risks if r.get('severity') == 'CRITICAL')
        high_count = sum(1 for r in risks if r.get('severity') == 'HIGH')
        medium_count = sum(1 for r in risks if r.get('severity') == 'MEDIUM')
        
        if critical_count > 0:
            overall = 'CRITICAL'
            summary = f'{critical_count} critical issue(s) detected. Seek legal advice immediately.'
        elif high_count > 0:
            overall = 'HIGH'
            summary = f'{high_count} high-priority issue(s) detected. Review carefully and seek advice.'
        elif medium_count > 0:
            overall = 'MEDIUM'
            summary = f'{medium_count} issue(s) detected. Review and consider seeking advice.'
        else:
            overall = 'LOW'
            summary = 'No significant issues detected'
        
        return {
            'overall_risk': overall,
            'critical_count': critical_count,
            'high_count': high_count,
            'medium_count': medium_count,
            'total_issues': len(risks),
            'summary': summary
        }
    
    def _generate_recommendations_regex(self, risks: List[Dict]) -> List[str]:
        """Generate recommendations based on detected risks"""
        recommendations = []
        
        for risk in risks:
            if risk['issue_type'] == 'MISSING_DEPOSIT_SCHEME':
                recommendations.append(
                    "Ensure your deposit is protected in a government-approved scheme within 30 days"
                )
            elif risk['issue_type'] == 'POTENTIAL_FEES':
                recommendations.append(
                    "Review all fees carefully. Many fees are now prohibited under the Tenant Fees Act 2019"
                )
            elif risk['issue_type'] == 'UNCLEAR_NOTICE_PERIOD':
                recommendations.append(
                    "Clarify the notice period requirements with your landlord in writing"
                )
        
        if not recommendations:
            recommendations.append("Have a legal professional review this document")
        
        return recommendations
    
    def _extract_entities_ml(self, text: str) -> Dict:
        """Placeholder for ML-based entity extraction"""
        # This would use actual ML models
        return {}
    
    def _generate_recommendations(self, patterns: Dict) -> List[str]:
        """Generate recommendations from patterns (legacy method)"""
        recommendations = []
        
        issues = patterns.get('issues', []) if isinstance(patterns, dict) else patterns
        for issue in issues:
            if issue.get('severity') == 'HIGH':
                recommendations.append(
                    f"Address {issue.get('issue_type', 'issue')} immediately"
                )
        
        return recommendations or ["Document appears compliant"]

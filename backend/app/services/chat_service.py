"""
Intelligent Chat Service
Provides human-like legal advice responses
"""
import re
from app.services.ml_service import MLService


class ChatService:
    """Intelligent chat service for housing law advice"""
    
    @staticmethod
    def detect_intent(message):
        """
        Detect user intent from message with validation
        
        Args:
            message: User message string
            
        Returns:
            dict with intent type and confidence
        """
        # Validate input
        if message is None:
            return {'intent': 'general_question', 'confidence': 0.1}
        
        if not isinstance(message, str):
            return {'intent': 'general_question', 'confidence': 0.1}
        
        # Strip and check length
        message = message.strip()
        
        if not message:
            return {'intent': 'general_question', 'confidence': 0.1}
        
        # Very short messages default to general question
        if len(message) < 3:
            return {'intent': 'general_question', 'confidence': 0.3}
        
        message_lower = message.lower()
        
        intents = {
            'document_analysis': [
                r'analyze.*document',
                r'check.*clause',
                r'review.*contract',
                r'look at.*agreement',
                r'is this.*fair',
                r'is this.*legal',
                r'can.*landlord.*do this',
                r'says.*in.*contract'
            ],
            'deposit_question': [
                r'deposit',
                r'security.*deposit',
                r'get.*money.*back',
                r'refund',
                r'protection.*scheme',
                r'how much.*deposit'
            ],
            'repair_question': [
                r'repair',
                r'fix',
                r'broken',
                r'maintenance',
                r'heating.*not.*work',
                r'leak',
                r'damp',
                r'mold',
                r'who.*responsible'
            ],
            'eviction_question': [
                r'evict',
                r'kick.*out',
                r'leave.*property',
                r'notice.*to.*quit',
                r'section 21',
                r'section 8',
                r'end.*tenancy'
            ],
            'rent_question': [
                r'rent.*increase',
                r'raise.*rent',
                r'pay.*more.*rent',
                r'rent.*too.*high',
                r'afford.*rent'
            ],
            'rights_question': [
                r'what.*are.*my.*rights',
                r'tenant.*rights',
                r'can.*i',
                r'am.*i.*allowed',
                r'legal.*rights',
                r'pet',
                r'pets',
                r'dog',
                r'cat',
                r'animal',
                r'landlord.*don\'t.*permit',
                r'landlord.*won\'t.*allow',
                r'not.*allowed.*to',
                r'garden',
                r'balcony',
                r'parking',
                r'amenity',
                r'amenities',
                r'use.*of',
                r'access.*to',
                r'new.*rule',
                r'added.*rule',
                r'changed.*rule'
            ],
            'complaint': [
                r'landlord.*not',
                r'landlord.*won\'t',
                r'landlord.*refuses',
                r'problem.*with.*landlord',
                r'harassment',
                r'threatening'
            ],
            'general_question': [
                r'what.*is',
                r'how.*does',
                r'explain',
                r'tell.*me.*about',
                r'information.*about'
            ]
        }
        
        try:
            for intent, patterns in intents.items():
                for pattern in patterns:
                    if re.search(pattern, message_lower):
                        return {'intent': intent, 'confidence': 0.8}
            
            # Check if message contains document text (long text)
            if len(message) > 100 and any(word in message_lower for word in ['tenant', 'landlord', 'agreement', 'property', 'rent']):
                return {'intent': 'document_analysis', 'confidence': 0.9}
        except Exception as e:
            print(f"Error detecting intent: {e}")
            return {'intent': 'general_question', 'confidence': 0.5}
        
        return {'intent': 'general_question', 'confidence': 0.5}
    
    @staticmethod
    def extract_context(message):
        """Extract relevant context from message"""
        context = {
            'has_amount': False,
            'has_timeframe': False,
            'is_urgent': False,
            'mentions_law': False
        }
        
        # Check for amounts
        if re.search(r'£\d+', message) or re.search(r'\d+.*pound', message.lower()):
            context['has_amount'] = True
        
        # Check for timeframes
        if re.search(r'\d+.*day|week|month|year', message.lower()):
            context['has_timeframe'] = True
        
        # Check for urgency
        urgent_words = ['urgent', 'emergency', 'immediately', 'asap', 'now', 'today']
        if any(word in message.lower() for word in urgent_words):
            context['is_urgent'] = True
        
        # Check for legal references
        legal_terms = ['section 21', 'section 8', 'act', 'law', 'legal', 'court']
        if any(term in message.lower() for term in legal_terms):
            context['mentions_law'] = True
        
        return context
    
    @staticmethod
    def generate_response(message, conversation_history=None):
        """
        Generate intelligent, human-like response with validation
        
        Args:
            message: User's message
            conversation_history: Previous messages for context
            
        Returns:
            dict with response and metadata
        """
        # Validate input
        if message is None or not isinstance(message, str):
            return {
                'response': "I'm sorry, I didn't receive a valid message. Could you please try again?",
                'intent': 'error',
                'needs_followup': True
            }
        
        message = message.strip()
        
        if not message:
            return {
                'response': "I'm here to help! Please ask me a question about housing law, tenant rights, or share a document clause you'd like me to review.",
                'intent': 'general_question',
                'needs_followup': True
            }
        
        # Limit message length
        max_length = 50000
        if len(message) > max_length:
            return {
                'response': f"Your message is too long (maximum {max_length} characters). Please break it into smaller parts or share the most important sections.",
                'intent': 'error',
                'needs_followup': True
            }
        
        try:
            # Detect intent
            intent_data = ChatService.detect_intent(message)
            intent = intent_data['intent']
            
            # Extract context
            context = ChatService.extract_context(message)
            
            # Check conversation history for context
            previous_topic = None
            if conversation_history and len(conversation_history) > 0:
                # Get the last assistant message to understand context
                for msg in reversed(conversation_history):
                    if msg.get('role') == 'assistant' and msg.get('metadata'):
                        previous_topic = msg['metadata'].get('intent')
                        break
            
            # SHORT MESSAGES: Treat as conversational questions, not document analysis
            # Only analyze as document if it's clearly document text (long, formal, contains clauses)
            is_document_text = (
                len(message) > 200 and 
                any(word in message.lower() for word in ['hereby', 'agreement', 'clause', 'tenant shall', 'landlord shall', 'witnesseth'])
            )
            
            # If message looks like document text, analyze it
            if is_document_text:
                return ChatService._handle_document_analysis(message, context)
            
            # Handle specific intents (conversational)
            if intent == 'deposit_question':
                return ChatService._handle_deposit_question(message, context)
            elif intent == 'repair_question':
                return ChatService._handle_repair_question(message, context)
            elif intent == 'eviction_question':
                return ChatService._handle_eviction_question(message, context)
            elif intent == 'rent_question':
                return ChatService._handle_rent_question(message, context)
            elif intent == 'rights_question':
                return ChatService._handle_rights_question(message, context)
            elif intent == 'complaint':
                return ChatService._handle_complaint(message, context)
            else:
                # Check if it's a follow-up question based on previous topic
                if previous_topic and previous_topic != 'general_question':
                    # Route to the same handler as previous topic
                    if previous_topic == 'deposit_question':
                        return ChatService._handle_deposit_question(message, context)
                    elif previous_topic == 'repair_question':
                        return ChatService._handle_repair_question(message, context)
                    elif previous_topic == 'eviction_question':
                        return ChatService._handle_eviction_question(message, context)
                    elif previous_topic == 'rent_question':
                        return ChatService._handle_rent_question(message, context)
                    elif previous_topic == 'rights_question':
                        return ChatService._handle_rights_question(message, context)
                
                return ChatService._handle_general_question(message, context)
        except Exception as e:
            print(f"Error generating response: {e}")
            return {
                'response': "I apologize, but I encountered an error processing your message. Please try rephrasing your question or contact support if the issue persists.",
                'intent': 'error',
                'needs_followup': True
            }
    
    @staticmethod
    def _handle_document_analysis(message, context):
        """Analyze document text"""
        try:
            # Use ML service to analyze
            analysis = MLService.analyze_text(message)
            
            if not analysis.get('success'):
                return {
                    'response': "I'd be happy to review that for you, but I'm having trouble analyzing the text right now. Could you try rephrasing or breaking it into smaller sections?",
                    'intent': 'document_analysis',
                    'needs_followup': True
                }
            
            # Build human-like response
            response = "I've reviewed the text you shared. Let me break down what I found:\n\n"
            
            # Document type
            if analysis.get('classification'):
                doc_type = analysis['classification']['category'].replace('_', ' ').title()
                confidence = analysis['classification']['confidence']
                response += f"📋 **Document Type**: This appears to be a {doc_type}.\n\n"
            
            # Issues found
            issues = analysis.get('detected_issues', [])
            if issues:
                response += f"⚠️ **Concerns Found**: I've identified {len(issues)} potential issue(s) that need your attention:\n\n"
                
                for i, issue in enumerate(issues[:5], 1):  # Limit to top 5
                    severity = issue['severity']
                    issue_name = issue['issue'].replace('_', ' ').title()
                    
                    emoji = '🚨' if severity == 'CRITICAL' else '⚠️' if severity == 'HIGH' else 'ℹ️'
                    response += f"{emoji} **{i}. {issue_name}** ({severity})\n"
                    response += f"   *What I found*: \"{issue['matched_text'][:80]}...\"\n"
                    response += f"   *Why this matters*: {issue['explanation']}\n\n"
                
                # Severity assessment
                severity_analysis = analysis.get('severity_analysis', {})
                if severity_analysis.get('overall_risk') == 'CRITICAL':
                    response += "🚨 **My Advice**: This is serious. I strongly recommend you don't sign this document without getting professional legal advice first. "
                    response += "Contact Shelter (0808 800 4444) or Citizens Advice (0800 144 8848) immediately.\n\n"
                elif severity_analysis.get('overall_risk') == 'HIGH':
                    response += "⚠️ **My Advice**: These are significant concerns. Before proceeding, I'd recommend getting these clauses clarified or amended. "
                    response += "Consider speaking with Shelter or Citizens Advice for guidance.\n\n"
                else:
                    response += "ℹ️ **My Advice**: While these issues aren't critical, they're worth discussing with your landlord or getting clarified.\n\n"
                
                # Top recommendations
                recommendations = analysis.get('recommendations', [])
                if recommendations:
                    response += "**What You Should Do**:\n"
                    for rec in recommendations[:3]:
                        response += f"• {rec}\n"
            else:
                response += "✅ **Good News**: I didn't find any major red flags in this text. However, I always recommend having important legal documents reviewed by a professional.\n\n"
                response += "**Still, keep in mind**:\n"
                response += "• Make sure you understand every clause\n"
                response += "• Ask questions about anything unclear\n"
                response += "• Keep copies of all documents\n"
            
            response += "\n\nIs there anything specific you'd like me to explain further?"
            
            return {
                'response': response,
                'intent': 'document_analysis',
                'analysis': analysis,
                'needs_followup': False
            }
            
        except Exception as e:
            return {
                'response': "I'd love to help analyze that for you, but I'm having a technical issue right now. Could you try again, or ask me a specific question about what concerns you?",
                'intent': 'document_analysis',
                'needs_followup': True
            }
    
    @staticmethod
    def _handle_deposit_question(message, context):
        """Handle deposit-related questions"""
        message_lower = message.lower()
        
        # Specific scenarios
        if 'non-refundable' in message_lower or 'not.*refund' in message_lower:
            response = "I'm glad you're asking about this! A 'non-refundable' deposit is actually **illegal** in the UK. Here's what you need to know:\n\n"
            response += "**The Law**:\n"
            response += "• All deposits MUST be refundable\n"
            response += "• Maximum deposit: 5 weeks' rent (or 6 weeks if annual rent exceeds £50,000)\n"
            response += "• Must be protected in a government-approved scheme within 30 days\n\n"
            response += "**What You Should Do**:\n"
            response += "• Don't pay a 'non-refundable' deposit\n"
            response += "• If you already paid, request an immediate refund\n"
            response += "• Report to Trading Standards if refused\n"
            response += "• Contact Shelter (0808 800 4444) for support\n\n"
            response += "Would you like me to explain more about deposit protection schemes?"
            
        elif 'how much' in message_lower or 'maximum' in message_lower:
            response = "Great question! Let me explain the deposit limits:\n\n"
            response += "**Maximum Deposit Amounts**:\n"
            response += "• Standard: 5 weeks' rent\n"
            response += "• High-value properties (annual rent over £50,000): 6 weeks' rent\n\n"
            response += "**Example**: If your monthly rent is £1,000:\n"
            response += "• Annual rent: £12,000\n"
            response += "• Maximum deposit: £1,153 (5 weeks)\n\n"
            response += "**Important**: Any amount above this is illegal under the Tenant Fees Act 2019.\n\n"
            response += "Is your landlord asking for more than this?"
            
        elif 'protection' in message_lower or 'scheme' in message_lower:
            response = "Deposit protection is crucial! Here's what you need to know:\n\n"
            response += "**The Rules**:\n"
            response += "• Your landlord MUST protect your deposit in a government-approved scheme\n"
            response += "• This must be done within 30 days of receiving your deposit\n"
            response += "• You must receive a certificate with scheme details\n\n"
            response += "**The Three Approved Schemes**:\n"
            response += "1. Deposit Protection Service (DPS)\n"
            response += "2. MyDeposits\n"
            response += "3. Tenancy Deposit Scheme (TDS)\n\n"
            response += "**If Not Protected**:\n"
            response += "• You can claim 1-3 times the deposit amount\n"
            response += "• Landlord cannot evict you using Section 21\n"
            response += "• Contact Shelter for help making a claim\n\n"
            response += "Have you received your deposit protection certificate?"
            
        elif 'get.*back' in message_lower or 'return' in message_lower:
            response = "Getting your deposit back can be stressful, but you have rights! Here's what you should know:\n\n"
            response += "**Your Rights**:\n"
            response += "• You're entitled to your full deposit back unless there's legitimate damage\n"
            response += "• Normal wear and tear doesn't count\n"
            response += "• Landlord must provide evidence of any deductions\n\n"
            response += "**The Process**:\n"
            response += "1. Do a thorough check-out inspection\n"
            response += "2. Take photos/videos of the property's condition\n"
            response += "3. Compare with check-in inventory\n"
            response += "4. Dispute any unfair deductions through the protection scheme\n\n"
            response += "**If There's a Dispute**:\n"
            response += "• Use the free Alternative Dispute Resolution (ADR) service\n"
            response += "• The scheme will make an independent decision\n"
            response += "• This is free and usually takes 2-4 weeks\n\n"
            response += "Are you currently in a dispute about your deposit?"
            
        else:
            response = "I'm here to help with your deposit question! Deposits are one of the most common issues tenants face.\n\n"
            response += "**Key Things to Know**:\n"
            response += "• Maximum: 5 weeks' rent (usually)\n"
            response += "• Must be refundable\n"
            response += "• Must be protected in approved scheme\n"
            response += "• You get it back at end of tenancy (minus legitimate deductions)\n\n"
            response += "Could you tell me more specifically what you'd like to know? For example:\n"
            response += "• Is the amount fair?\n"
            response += "• Is it protected?\n"
            response += "• How to get it back?\n"
            response += "• Disputing deductions?"
        
        return {
            'response': response,
            'intent': 'deposit_question',
            'needs_followup': True
        }
    
    @staticmethod
    def _handle_repair_question(message, context):
        """Handle repair-related questions"""
        message_lower = message.lower()
        
        if context['is_urgent']:
            response = "I understand this is urgent. Let me help you quickly:\n\n"
            response += "**Emergency Repairs** (immediate danger):\n"
            response += "• No heating in winter\n"
            response += "• No hot water\n"
            response += "• Serious leaks\n"
            response += "• Gas leaks\n"
            response += "• Electrical hazards\n\n"
            response += "**What to Do RIGHT NOW**:\n"
            response += "1. Contact your landlord immediately (call, don't email)\n"
            response += "2. If gas leak: Call National Gas Emergency: 0800 111 999\n"
            response += "3. If electrical danger: Turn off at mains if safe\n"
            response += "4. If landlord doesn't respond within 24 hours: Contact your local council's emergency repairs line\n\n"
            response += "**Document Everything**:\n"
            response += "• Take photos/videos\n"
            response += "• Keep records of all contact attempts\n"
            response += "• Note dates and times\n\n"
            response += "What specific repair issue are you facing?"
        else:
            response = "Let me explain repair responsibilities - this is really important:\n\n"
            response += "**Landlord's Responsibilities** (by law):\n"
            response += "• Structure and exterior (walls, roof, windows, doors)\n"
            response += "• Heating and hot water systems\n"
            response += "• Plumbing and sanitation\n"
            response += "• Electrical wiring\n"
            response += "• Gas appliances and safety\n\n"
            response += "**Your Responsibilities**:\n"
            response += "• Minor repairs (like changing light bulbs)\n"
            response += "• Damage you caused\n"
            response += "• Keeping the property clean\n\n"
            response += "**How to Request Repairs**:\n"
            response += "1. Report in writing (email is best)\n"
            response += "2. Be specific about the problem\n"
            response += "3. Give reasonable access for repairs\n"
            response += "4. Keep copies of all communications\n\n"
            response += "**If Landlord Ignores You**:\n"
            response += "• Send a formal letter giving 14 days to respond\n"
            response += "• Contact your local council's Environmental Health team\n"
            response += "• They can inspect and force repairs\n"
            response += "• You're protected from retaliatory eviction for 6 months\n\n"
            response += "What repair issue are you dealing with?"
        
        return {
            'response': response,
            'intent': 'repair_question',
            'needs_followup': True
        }
    
    @staticmethod
    def _handle_eviction_question(message, context):
        """Handle eviction-related questions"""
        message_lower = message.lower()
        
        if 'section 21' in message_lower:
            response = "This is really important - **Section 21 no-fault evictions were ABOLISHED in October 2025**!\n\n"
            response += "**What This Means**:\n"
            response += "• Section 21 notices are NO LONGER VALID\n"
            response += "• You cannot be evicted without a specific reason\n"
            response += "• Landlords must use Section 8 with valid grounds\n\n"
            response += "**If You Received a Section 21 Notice**:\n"
            response += "• You can IGNORE it - it has no legal force\n"
            response += "• Continue paying rent as normal\n"
            response += "• Stay in your property\n"
            response += "• Contact Shelter immediately: 0808 800 4444\n\n"
            response += "**If Landlord Tries to Force You Out**:\n"
            response += "• This is ILLEGAL eviction\n"
            response += "• Call the police (999)\n"
            response += "• Contact your local council\n"
            response += "• You may be entitled to compensation\n\n"
            response += "Don't let anyone pressure you to leave based on a Section 21 notice. You have strong legal protection now."
            
        elif any(word in message_lower for word in ['kick out', 'force', 'leave immediately']):
            response = "⚠️ This sounds like it could be illegal eviction. Let me explain your rights:\n\n"
            response += "**Legal Eviction Process**:\n"
            response += "• Landlord must have valid grounds (Section 8)\n"
            response += "• Must give proper notice (usually 2 months)\n"
            response += "• Must get a court order\n"
            response += "• Only court bailiffs can remove you\n\n"
            response += "**Illegal Eviction** (any of these):\n"
            response += "• Changing locks\n"
            response += "• Removing your belongings\n"
            response += "• Cutting off utilities\n"
            response += "• Harassment or threats\n"
            response += "• Forcing entry\n\n"
            response += "**If This Is Happening**:\n"
            response += "1. Call police immediately (999) - it's a criminal offense\n"
            response += "2. Contact Shelter: 0808 800 4444\n"
            response += "3. Contact your local council's housing team\n"
            response += "4. Document everything (photos, recordings, witnesses)\n\n"
            response += "**You Can Claim**:\n"
            response += "• Compensation for illegal eviction\n"
            response += "• Right to return to property\n"
            response += "• Damages for distress\n\n"
            response += "Are you currently being threatened with eviction?"
            
        else:
            response = "Eviction is a serious matter, but you have strong protections. Let me explain:\n\n"
            response += "**Current Law (Renters Rights Act 2025)**:\n"
            response += "• No-fault evictions (Section 21) are ABOLISHED\n"
            response += "• Landlords need a valid reason to evict you\n"
            response += "• Must follow proper legal process\n\n"
            response += "**Valid Reasons for Eviction** (Section 8):\n"
            response += "• Rent arrears (usually 2+ months)\n"
            response += "• Antisocial behavior\n"
            response += "• Damage to property\n"
            response += "• Landlord wants to sell (with conditions)\n"
            response += "• Landlord/family wants to move in (with conditions)\n\n"
            response += "**The Process**:\n"
            response += "1. Written notice (usually 2 months)\n"
            response += "2. Court hearing\n"
            response += "3. Court order (if granted)\n"
            response += "4. Bailiff appointment\n"
            response += "5. Only then can you be removed\n\n"
            response += "**Your Rights**:\n"
            response += "• Challenge the eviction in court\n"
            response += "• Stay until court orders otherwise\n"
            response += "• Get legal aid if eligible\n"
            response += "• Protected from retaliatory eviction\n\n"
            response += "What's your specific situation? Have you received a notice?"
        
        return {
            'response': response,
            'intent': 'eviction_question',
            'needs_followup': True
        }
    
    @staticmethod
    def _handle_rent_question(message, context):
        """Handle rent-related questions"""
        response = "Rent increases can be worrying. Let me explain your rights:\n\n"
        response += "**The Rules**:\n"
        response += "• Rent can only be increased once per year (unless your contract says otherwise)\n"
        response += "• You must receive proper notice (usually 1 month for monthly tenancies)\n"
        response += "• Increase must be 'fair and realistic'\n\n"
        response += "**How Increases Work**:\n"
        response += "• Fixed-term tenancy: Only if contract allows it\n"
        response += "• Periodic tenancy: Landlord can propose increase\n"
        response += "• You can negotiate or challenge\n\n"
        response += "**If You Think It's Unfair**:\n"
        response += "• Compare with similar properties in your area (check Rightmove, Zoopla)\n"
        response += "• Negotiate with your landlord\n"
        response += "• Apply to tribunal if you can't agree\n\n"
        response += "**Tribunal Process**:\n"
        response += "• Free to apply\n"
        response += "• They'll assess if increase is fair\n"
        response += "• Decision is binding\n"
        response += "• Usually takes 6-8 weeks\n\n"
        response += "**If You Can't Afford It**:\n"
        response += "• Check if eligible for housing benefit/Universal Credit\n"
        response += "• Contact Shelter for advice: 0808 800 4444\n"
        response += "• Negotiate payment plan\n"
        response += "• Don't just stop paying - this could lead to eviction\n\n"
        response += "How much is your rent increasing by?"
        
        return {
            'response': response,
            'intent': 'rent_question',
            'needs_followup': True
        }
    
    @staticmethod
    def _handle_rights_question(message, context):
        """Handle general rights questions"""
        message_lower = message.lower()
        
        # Check if it's about garden/amenities/access
        if any(word in message_lower for word in ['garden', 'balcony', 'parking', 'amenity', 'amenities', 'use of', 'access to']):
            response = "That's a great question about your rights to use property amenities! Let me explain:\n\n"
            response += "**Your Rights to Amenities**:\n\n"
            response += "**The Law**:\n"
            response += "• If your tenancy agreement includes access to amenities (garden, parking, etc.), you have a legal right to use them\n"
            response += "• Landlord cannot arbitrarily remove these rights during your tenancy\n"
            response += "• Any changes must be agreed in writing\n\n"
            
            if 'garden' in message_lower:
                response += "**Specifically About Gardens**:\n"
                response += "• If your agreement says you can use the garden, you can use it\n"
                response += "• Landlord can't suddenly ban you from using it\n"
                response += "• You're usually responsible for basic maintenance (mowing, weeding)\n"
                response += "• Landlord is responsible for major work (fences, trees, structures)\n\n"
            
            if 'new rule' in message_lower or 'added rule' in message_lower or 'changed' in message_lower:
                response += "**About New Rules**:\n"
                response += "• Landlord CANNOT unilaterally change your tenancy terms mid-contract\n"
                response += "• Any changes require your written agreement\n"
                response += "• If you're on a fixed-term tenancy, terms are locked until it ends\n"
                response += "• Even on periodic tenancy, changes need proper notice and your consent\n\n"
                
                response += "**What You Should Do**:\n"
                response += "1. Check your tenancy agreement - what does it say about the garden/amenity?\n"
                response += "2. If it's included, you have the right to use it\n"
                response += "3. Respond to your landlord in writing:\n"
                response += "   - Reference your tenancy agreement\n"
                response += "   - State that you do not agree to this change\n"
                response += "   - Assert your right to continue using the amenity\n"
                response += "4. Keep all communications in writing\n\n"
                
                response += "**If Landlord Persists**:\n"
                response += "• This could be breach of contract\n"
                response += "• You can report to your local council\n"
                response += "• Contact Shelter for advice: 0808 800 4444\n"
                response += "• You may be able to claim compensation\n"
                response += "• Protected from retaliatory eviction for 6 months\n\n"
                
                response += "**Important**: Don't let your landlord bully you into accepting changes you didn't agree to. Your tenancy agreement is a legal contract that protects both parties.\n\n"
            else:
                response += "**What You Should Do**:\n"
                response += "1. Check your tenancy agreement carefully\n"
                response += "2. Look for clauses about amenities and access\n"
                response += "3. If it's mentioned, you have the right to use it\n"
                response += "4. If landlord is restricting access, challenge it in writing\n\n"
            
            response += "Does your tenancy agreement specifically mention the garden/amenity in question?"
            
            return {
                'response': response,
                'intent': 'rights_question',
                'needs_followup': True
            }
        
        # Check if it's specifically about pets
        if any(word in message_lower for word in ['pet', 'pets', 'dog', 'cat', 'animal']):
            response = "Great question about pets! The law changed recently and you now have MORE rights:\n\n"
            response += "**The New Pet Rights (Renters Rights Act 2025)**:\n\n"
            response += "**What Changed**:\n"
            response += "• Landlords can NO LONGER have blanket 'no pets' policies\n"
            response += "• They must consider each pet request reasonably\n"
            response += "• Can only refuse with a good reason\n\n"
            response += "**Your Rights**:\n"
            response += "• You can request to have a pet\n"
            response += "• Landlord must respond within 28 days\n"
            response += "• If they refuse, they must give a valid reason\n"
            response += "• You can challenge unreasonable refusals\n\n"
            response += "**Valid Reasons to Refuse**:\n"
            response += "• Property is unsuitable (e.g., too small)\n"
            response += "• Building rules prohibit pets\n"
            response += "• Pet would cause damage to specific features\n"
            response += "• Allergies of other residents (in shared housing)\n\n"
            response += "**Invalid Reasons** (landlord can't refuse for these):\n"
            response += "• 'I don't like pets'\n"
            response += "• 'Pets always cause damage'\n"
            response += "• 'My insurance doesn't cover it' (they must get appropriate insurance)\n"
            response += "• No reason given\n\n"
            response += "**What You Should Do**:\n"
            response += "1. Make a formal written request\n"
            response += "2. Provide details about your pet (type, size, temperament)\n"
            response += "3. Offer to pay pet deposit (if reasonable)\n"
            response += "4. Offer references from previous landlords\n\n"
            response += "**If Landlord Refuses**:\n"
            response += "• Ask for the reason in writing\n"
            response += "• Challenge if it's not valid\n"
            response += "• Contact Shelter for advice: 0808 800 4444\n"
            response += "• Consider tribunal if needed\n\n"
            response += "**Important**: If you already have a pet and your landlord is trying to make you get rid of it, they need a valid reason and must follow proper process.\n\n"
            response += "Do you have a specific situation with your landlord and pets?"
            
            return {
                'response': response,
                'intent': 'rights_question',
                'needs_followup': True
            }
        
        # General rights question
        response = "I'm glad you're asking about your rights! As a tenant in the UK, you have strong legal protections:\n\n"
        response += "**Your Core Rights**:\n\n"
        response += "**1. Right to a Safe Home**\n"
        response += "• Property must meet health and safety standards\n"
        response += "• Landlord must do repairs\n"
        response += "• Gas and electrical safety certificates required\n\n"
        response += "**2. Right to Quiet Enjoyment**\n"
        response += "• Landlord can't enter without 24 hours notice (except emergencies)\n"
        response += "• No harassment\n"
        response += "• Privacy in your home\n\n"
        response += "**3. Deposit Protection**\n"
        response += "• Deposit must be protected in approved scheme\n"
        response += "• Maximum 5 weeks' rent\n"
        response += "• Must be refundable\n\n"
        response += "**4. Protection from Unfair Eviction**\n"
        response += "• No-fault evictions abolished\n"
        response += "• Proper legal process required\n"
        response += "• Can't be evicted for reporting repairs\n\n"
        response += "**5. Right to Challenge**\n"
        response += "• Challenge unfair rent increases\n"
        response += "• Dispute deposit deductions\n"
        response += "• Report poor conditions\n\n"
        response += "**6. Right to Have Pets** (New!)\n"
        response += "• Landlords can't have blanket pet bans\n"
        response += "• Must consider requests reasonably\n"
        response += "• Can only refuse with good reason\n\n"
        response += "Is there a specific right you'd like to know more about?"
        
        return {
            'response': response,
            'intent': 'rights_question',
            'needs_followup': True
        }
    
    @staticmethod
    def _handle_complaint(message, context):
        """Handle complaints about landlord"""
        response = "I'm sorry you're having problems with your landlord. Let me help you understand your options:\n\n"
        
        if context['is_urgent']:
            response += "**This Sounds Urgent** - Here's what to do:\n\n"
            response += "**If You're Being Harassed or Threatened**:\n"
            response += "• Call police if you feel unsafe (999)\n"
            response += "• Contact Shelter immediately: 0808 800 4444\n"
            response += "• Document everything (photos, recordings, witnesses)\n"
            response += "• Contact your local council's housing team\n\n"
        
        response += "**Steps to Take**:\n\n"
        response += "**1. Document Everything**\n"
        response += "• Keep all emails, texts, letters\n"
        response += "• Take photos/videos\n"
        response += "• Note dates, times, witnesses\n"
        response += "• Keep a diary of incidents\n\n"
        response += "**2. Communicate in Writing**\n"
        response += "• Email is best (creates paper trail)\n"
        response += "• Be clear and factual\n"
        response += "• State what you want to happen\n"
        response += "• Give reasonable deadline\n\n"
        response += "**3. Escalate if Needed**\n"
        response += "• Contact landlord's letting agent\n"
        response += "• Report to local council\n"
        response += "• Contact Shelter or Citizens Advice\n"
        response += "• Consider legal action\n\n"
        response += "**Your Protections**:\n"
        response += "• Protected from retaliatory eviction for 6 months after reporting issues\n"
        response += "• Harassment is a criminal offense\n"
        response += "• You can claim compensation\n\n"
        response += "**Get Help**:\n"
        response += "• Shelter: 0808 800 4444\n"
        response += "• Citizens Advice: 0800 144 8848\n"
        response += "• Local council housing team\n\n"
        response += "What specifically is your landlord doing that concerns you?"
        
        return {
            'response': response,
            'intent': 'complaint',
            'needs_followup': True
        }
    
    @staticmethod
    def _handle_general_question(message, context):
        """Handle general questions"""
        response = "I'm here to help you with any housing law questions! I can assist with:\n\n"
        response += "**Common Topics**:\n"
        response += "• 📄 Reviewing tenancy agreements and documents\n"
        response += "• 💰 Deposit questions and protection\n"
        response += "• 🔧 Repairs and maintenance issues\n"
        response += "• 🏠 Eviction notices and your rights\n"
        response += "• 💷 Rent increases and affordability\n"
        response += "• ⚖️ Your rights as a tenant\n"
        response += "• 😟 Landlord disputes and complaints\n\n"
        response += "**How I Can Help**:\n"
        response += "• Analyze documents for unfair clauses\n"
        response += "• Explain your legal rights in plain English\n"
        response += "• Provide specific advice for your situation\n"
        response += "• Direct you to the right support services\n\n"
        response += "**To Get Started**:\n"
        response += "• Ask me a specific question\n"
        response += "• Paste text from a document you want me to review\n"
        response += "• Tell me about a problem you're facing\n\n"
        response += "What would you like help with today?"
        
        return {
            'response': response,
            'intent': 'general_question',
            'needs_followup': True
        }

from . models import *

def get_customer_report_data(customer):
    """
    Get complete report data for a customer matching the API response format
    """
    if not customer:
        return None
    
    report_data = {
        'customer': {
            "name": customer.user.name,
            "email": customer.user.email,
            "house_image": customer.house_image.url if customer.house_image else None,
            "address": customer.address,
            "city": customer.city,
            "state": customer.state,
            "zip": customer.zip,
        },
        'principles': []
    }
    
    # Get all principles ordered
    principles = Principle.objects.all().order_by("order")
    
    def get_feedback_data(customer, category):
        """Helper function to get feedback data for a category"""
        try:
            feedback = Feedback.objects.get(customer=customer, category=category)
            
            # Get feedback images using the ManyToMany relationship
            feedback_images = feedback.images.all()
            images_data = []
            for img in feedback_images:
                images_data.append({
                    'id': img.id,
                    'created_at': img.created_at.isoformat(),
                    'updated_at': img.updated_at.isoformat(),
                    'image': img.image.url if img.image else None
                })
            
            return {
                'id': feedback.id,
                'note': feedback.note or '',
                'images': images_data
            }
        except Feedback.DoesNotExist:
            return None
        except Exception as e:
            # Log the specific error for debugging
            print(f"Error retrieving feedback for category {category.id}: {e}")
            return None
    
    for principle in principles:
        principle_data = {
            'principle': {
                'id': principle.id,
                'created_at': principle.created_at.isoformat() if hasattr(principle, 'created_at') else None,
                'updated_at': principle.updated_at.isoformat() if hasattr(principle, 'updated_at') else None,
                'name': principle.name,
                'order': principle.order,
                'key': getattr(principle, 'key', '')
            },
            'categories': []
        }
        
        # Get main categories (parent categories) for this principle
        main_categories = Category.objects.filter(
            principle=principle, 
            parent__isnull=True
        ).order_by('order')
        
        for main_category in main_categories:
            # Check if main category is answered
            main_category_answered = SelectedOption.objects.filter(
                customer=customer,
                category=main_category,
                selected=True
            ).exists()
            
            # Check if any subcategory is answered
            subcategory_answered = SelectedOption.objects.filter(
                customer=customer,
                category__parent=main_category,
                selected=True
            ).exists()
            
            is_answered = main_category_answered or subcategory_answered
            
            # Check if category is applicable
            try:
                applicability = CategoryApplicability.objects.get(
                    customer=customer, 
                    category=main_category
                )
                applicable = applicability.applicable
            except CategoryApplicability.DoesNotExist:
                applicable = True
            
            # Get feedback for main category using helper function
            feedback_data = get_feedback_data(customer, main_category)
            
            category_data = {
                'id': main_category.id,
                'name': main_category.name,
                'order': main_category.order,
                'is_answered': is_answered,
                'feedback': feedback_data,
                'options': [],
                'subcategories': [],
                'applicable': applicable
            }
            
            # Get options for main category
            main_category_options = Option.objects.filter(category=main_category)
            for option in main_category_options:
                is_selected = SelectedOption.objects.filter(
                    customer=customer,
                    option=option,
                    selected=True
                ).exists()
                
                option_data = {
                    'id': option.id,
                    'text': option.text,
                    'is_selected': is_selected
                }
                category_data['options'].append(option_data)
            
            # Get subcategories
            subcategories = Category.objects.filter(parent=main_category).order_by('order')
            for subcategory in subcategories:
                # Check subcategory applicability
                try:
                    sub_applicability = CategoryApplicability.objects.get(
                        customer=customer, 
                        category=subcategory
                    )
                    sub_applicable = sub_applicability.applicable
                except CategoryApplicability.DoesNotExist:
                    sub_applicable = True
                
                # Check if subcategory is answered
                sub_answered = SelectedOption.objects.filter(
                    customer=customer,
                    category=subcategory,
                    selected=True
                ).exists()
                
                # Get feedback for subcategory using helper function
                sub_feedback_data = get_feedback_data(customer, subcategory)
                
                subcategory_data = {
                    'id': subcategory.id,
                    'name': subcategory.name,
                    'order': subcategory.order,
                    'is_answered': sub_answered,
                    'feedback': sub_feedback_data,
                    'options': [],
                    'subcategories': [],  # Empty as per your structure
                    'applicable': sub_applicable
                }
                
                # Get options for subcategory
                subcategory_options = Option.objects.filter(category=subcategory)
                for option in subcategory_options:
                    is_selected = SelectedOption.objects.filter(
                        customer=customer,
                        option=option,
                        selected=True
                    ).exists()
                    
                    option_data = {
                        'id': option.id,
                        'text': option.text,
                        'is_selected': is_selected
                    }
                    subcategory_data['options'].append(option_data)
                
                category_data['subcategories'].append(subcategory_data)
            
            principle_data['categories'].append(category_data)
        
        report_data['principles'].append(principle_data)
    
    return report_data
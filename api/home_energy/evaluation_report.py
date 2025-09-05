from .models import *

def get_customer_home_energy_report(customer):
    """
    Generate a full home energy report for a given customer.
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
        'steps': []
    }

    # Get all steps ordered
    steps = Step.objects.all().order_by("order")

    def get_feedback_data(customer, question_group):
        """Helper to fetch feedback for a question group"""
        try:
            feedback = Feedback.objects.get(customer=customer, question_group=question_group)

            images_data = []
            for img in feedback.images.all():
                images_data.append({
                    'id': img.id,
                    'created_at': img.created_at.isoformat(),
                    'updated_at': img.updated_at.isoformat(),
                    'image': img.image.url if img.image else None
                })

            return {
                'id': feedback.id,
                'text': feedback.text or '',
                'images': images_data
            }
        except Feedback.DoesNotExist:
            return None
        except Exception as e:
            print(f"Error retrieving feedback for question_group {question_group.id}: {e}")
            return None

    for step in steps:
        step_data = {
            'step': {
                'id': step.id,
                'title': step.title,
                'order': step.order,
                'created_at': step.created_at.isoformat() if hasattr(step, 'created_at') else None,
                'updated_at': step.updated_at.isoformat() if hasattr(step, 'updated_at') else None,
            },
            'question_groups': []
        }

        question_groups = QuestionGroup.objects.filter(step=step)
        for qg in question_groups:
            feedback_data = get_feedback_data(customer, qg)

            qg_data = {
                'id': qg.id,
                'feedback': feedback_data,
                'questions': []
            }

            # Iterate over questions in the group
            for question in qg.question.all():
                # Get text answer
                try:
                    answer = Answer.objects.get(customer=customer, question=question)
                    answer_text = answer.text
                except Answer.DoesNotExist:
                    answer_text = None

                # Get options for this question
                options_data = []
                options = Option.objects.filter(question=question)
                has_option_selected = SelectedOptions.objects.filter(customer=customer, option__in=options).exists()

                for option in options:
                    is_selected = SelectedOptions.objects.filter(customer=customer, option=option).exists()

                    options_data.append({
                        'id': option.id,
                        'text': option.text,
                        'is_selected': is_selected
                    })

                question_data = {
                    'id': question.id,
                    'text': question.text,
                    'field_type': question.field_type,
                    'answer': answer_text,
                    'options': options_data,
                    'has_option_selected': has_option_selected
                }

                qg_data['questions'].append(question_data)

            step_data['question_groups'].append(qg_data)

        report_data['steps'].append(step_data)

    return report_data

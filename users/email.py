from djoser.email import ActivationEmail

class CustomActivationEmail(ActivationEmail):
    template_name = "email/custom_activation_email.html"

    def get_context_data(self):
        context = super().get_context_data()

        front_end_url = 'http://localhost:3000'
        uid = context.get('uid')
        token = context.get('token')
        
        context['url'] = f"{front_end_url}/activate/?uid={uid}&token={token}"
        return context
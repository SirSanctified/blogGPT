import os
import openai
from django.shortcuts import render
from django.contrib import messages
from main import forms


def home(request):
    return render(request, 'main/index.html')


def create_blog(request):
    template = 'main/create_blog.html'
    form = forms.BlogForm()
    
    if request.method == 'POST':
        form = forms.BlogForm(request.POST)
        key = os.getenv('OPENAI_API_KEY')
        openai.key = key
        
        blog_title = request.POST['title']

        # check if the title requested does not violate
        # OpenAI's Content Policy
        
        moderation = openai.Moderation.create(
            input = blog_title
        )
        
        if not moderation.results[0].flagged:
            # create an initial prompt that returns the list of sections (synopsis)
            # about a particular post title
            
            number_of_sections = int(request.POST['sections'])
            
            if number_of_sections > 10:
                number_of_sections = 10
            
            initial_prompt = f"I want to write a blog post titled {blog_title}. Write a list of {number_of_sections} points for this blog post in numbered list format."
            synopsis = openai.Completion.create(
                model = "text-davinci-003",
                prompt = initial_prompt,
                max_tokens = 2000,
                temperature = 0.7
            )
            
            synopsis = synopsis.choices[0].text
            
            print(synopsis)
    
            blog_sections = synopsis.strip().splitlines()
            
                                   
            blog_post = '<h2>' + blog_title + '</h2>'
            
            for section in blog_sections:
                section_prompt = f"""I want to write a blog post \
                titled {blog_title}. These are the sections of the blog:
                {synopsis.lstrip()}. 
                Write about the section {section} in a detailed an complete \
                way in 500 words minimum length."""
                
                section_detail = openai.Completion.create(
                model = "text-davinci-003",
                prompt = section_prompt,
                max_tokens = 3000,
                temperature = 0.7
                )
                
                section_detail = section_detail.choices[0].text.strip()
                
                blog_post += '<h4>' + section + '</h4>' + '<p>' + section_detail + '</p>'
            
            post = blog_post
                                    
            context = {
                "form": form,
                "post": post,
                "flagged": False
                }
            messages.success(request, "It took a little longer, but finally your blog is ready.")
            
            return render(request, template, context = context)
        
        else:
            messages.error(request, "Your input text was flagged as either violent, abusive or discriminatory. I'm sorry, I can't help you generate content that may hurt others in any way.")
            return render(request, template, {"form": form, "flagged": True})
    
    return render(request, template, {"form": form})
        
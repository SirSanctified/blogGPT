# BlogGPT

## Features

BlogGPT is a simple web application that uses GPT-3 to generate full-length blog posts. It only requires that the user enter the title of the blog and an optional number of sections they want in their blog post. The default number is 5 and the maximum supported number of sections is 10. This was is to reduce the number of API calls to OpenAI.

The title is moderated to make sure it does not violate the OpenAI's Content Policy. If the title is flagged to be violating it, the approprite message is returned back to the user without making the actual API call for content generation.

## Possible Improvements

At the moment, this is just a simple function handling the API calls in a synchronus fashion. The downside is that for as little as 5 blog sections, the total wait time may get to more than a minute at worst. The possible improvement is to make the API calls in an asynchronus way to speed up the response time.

More features can be added in the future such as personalised content and more.
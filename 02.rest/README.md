# Starting with REST

What we had before can not be truly considered a REST service. REST services
operate on collections of objects and we had none of these.  In this section
we shall build one.

Here are good primers on REST and REST API design best practices:

* https://restfulapi.net/
* https://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api

In this section we will make at least one deviation from those, so
be on a look out!

Review [some REST API examples](https://openclassrooms.com/en/courses/3432056-build-your-web-projects-with-rest-apis/3496011-identify-examples-of-rest-apis):

* [Instagram API](https://www.instagram.com/developer/endpoints/users/)
* [Gmail API](https://openclassrooms.com/en/courses/3432056-build-your-web-projects-with-rest-apis/3496011-identify-examples-of-rest-apis)
* [Google Drive REST API](https://cloud.google.com/storage/docs/json_api/v1/)
* [GitHub REST API](https://developer.github.com/v3/)

Farm API specified in [Farm.API.v01.md](Farm.API.v01.md).
I am not a farming domain expert.
But for my purposes at this stage such an API will do the job of
demonstrating the craft of building a REST server.

Then, check out the code in the [farm folder](farm/)!.

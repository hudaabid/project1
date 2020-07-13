When you run flask app the first page you get is the "register.html", where you are asked to login or signup.
The data is handeled in the psql table "register".

Then it is redirected to the success page for signup and login. From where the main page is accessed named as "page.html".
it has logout button also.

It has a "search bar" where you can enter the query for title,author and isbn. which then will be redirected to the book options page name "books.html".
Then on clicking the book title it is the redirected to the page of that particular book detail. named "book.html"

The book page has reviews from the goodread site, and also it gives the option to add the reviews for the book.

/api/isbn returns the json response
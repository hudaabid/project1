webpagespace.html is a main page includes general information about space.
This page includes bootstrap link for buttons that are linked to three different html pages planetpage.html,sunpage.html and moonpage.html.
It also includes a css file link to style the page. the css file is cssfilesstyle.css.
All these 4 html pages contain @media query, which changes color on smaller screen.

planetpage.html also includes bootstrap 4 link for the grid table, and a link to cssfilestyle.css
It has table, image, id and class selectors too. 
The table used in planetpage is styled by sass file named tablescss.scss which was compiled to a css file named csstablestyle.css

sunpage.html is another link which is directed through webpagespace.html, it includes the bootstrap link for container and sass inheritance is used here. 
using the file suninheritance.sass which is compiled then to suninheritance.css
it also uses the cssfilestyle.css file.

moonpage.html also contains bootstrap 4 link for container used in its coding and style sheet link cssfilestyle.css. it also contains image.

cssfilestyle.css has
h1
p
And it also has selectors:
h1,h2
ol li
p:: selection

Other selector that is a::before, is used in webpagespace.html for button.

in csstablestyle.css table th, table td selector is used. which is compiled by tablescss.scss

in suninheritance.css mag,var selector is used which is compiled by the sass file suninheritance.scss which has %message for inheritance using @extend %message syntax 

in variuos places in code the id and class are used
# Vulnérabilité côté serveur

## URL

Les images sont stockées dans un dossier var/www/images/your_image.jpg.
Si l'url n'est pas sécurisé, il est possibel d'obtenir des informations qui n'ont pas lieu d'être de base ...

Les caractères spéciaux sont encodés afin d'éviter des mauvaises interprétations. Par exemple, ' est encodé en %27.

##### Linux :
https://insecure-website.com/loadImage?filename=../../../etc/passwd

##### Windows : 
https://insecure-website.com/loadImage?filename=..\..\..\windows\win.ini

### Faille CRLF

L'utilisation d'un caractère de fin de ligne comme \n ou \r.

## Fonctionnalités sans restrictions
tips: regarder le code source des pages !!!

https://insecure-website.com/admin

https://insecure-website.com/robots.txt

https://insecure-website.com/administrator-panel

##### admin acess
Pour déterminer si un utilisateur possède certains droits, on lui confère un rôle. Celui-ci est déterminé/attribué via :
- un hidden field
- un cookie
- un preset query string parameter

Il est parfois possible de changer la valeur du cookie admin dans (Inspecter/Apllications/Cookies/...)

https://insecure-website.com/login/home.jsp?admin=true

https://insecure-website.com/login/home.jsp?role=1

##### horizontal acess

https://insecure-website.com/myaccount?id=123

On peut changer la valeur de l'id pour tomber sur un autre compte (IDOR).

On préfèrera utiliser des GUIs pour que les valeurs ne soient plus facilement prédictible.

## Vulnérabilités d'authentication

Authentication : procédé vérifiant si l'utilisateur est bien celui qui prétend être.

### Attaques

- Brute-force, attaque par dictionnaire

## SSRF (Server-Side Request Forgery)


Server-side request forgery is a web security vulnerability that allows an attacker to cause the server-side application to make requests to an unintended location.

In a typical SSRF attack, the attacker might cause the server to make a connection to internal-only services within the organization's infrastructure. In other cases, they may be able to force the server to connect to arbitrary external systems. This could leak sensitive data, such as authorization credentials.

Typiquement, on peut modifier l'adresse de stockAPI vers une adresse locale, nous permettant ainsi d'obtenir des accès supplémentaire.

##### Pourquoi ça marche ?

En fait, la personne qui est cencé accéder au serveur est une personne normalement de confiance.
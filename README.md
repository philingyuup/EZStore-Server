# EZStore-Server

##  Links
- [Client App](https://philingyuup.github.io/EZStore-Client/)
- [Client Repo](https://github.com/philingyuup/EZStore-Client)
- [API App](https://ezstore-server.herokuapp.com/)
- [API Repo](https://github.com/philingyuup/EZStore-Server)

## Intro
EZStore is an e-commerce store that is customizable through admin abilities given to owners or staff members of the store. EZStore-Server is a RESTful API built using Python, PostgresQL, and Django's REST framework. Below you'll find more information about the server as well as information on how to communicate with it.

## How to use API
Instructions for how to use the API is listed below this README file in the **Instructions** portion. You'll find information on how to access the ```users```, ```products```, and cloudinary routes.

## Planning Story
I wanted to make an e-commerce store that gives admin abilities for the owner and staff members of the site. The admin abilities include being able to edit the store, choose different templates/layouts, and upload products. Customers are also able to login and perform actions as a repeated customer (saved mailing address and credit cards). For the MVP, it'll just be the ability to CRUD products onto the page (as a staff member of the ecommerce store). Regular users (customers) won't be able to access the Admin page and only has read-only access to the server.

## Technologies Used
- Django
- PostgresQL
- Python
- React
- React-Bootstrap
- Axios
- Cloudinary (image hosting)

## Future Features
- Database for the store (edit store)
- Different layouts for the store (owner's choose)
- Stripe integration (for payment)
- USPS Webtools (for shipment)
- Expand ```user``` and ```product``` databases

## Issues Encountered
This was my first *real* attempt (project) at using Django and Python. Python was friendly to get along with (loved the windows compatibility). For all my issues relating to Windows, ```winpty``` as a prefix before command lines (i.e. ```winpty python manage.py migrate```) fixed the issue. You can find more information about ```winpty``` on [github.com/rprichard/winpty](https://github.com/rprichard/winpty). Windows issues included all Python commands and Postgres commands. Django REST framework was a little difficult to work with (documentation isn't noob friendly) but there's a lot of stackoverflow responses to Django issues/questions. Django's admin page is also amazing and a great feature. There were some deployment issues relating to CORS and it was solved by adding the production url to the development ```cors_origin_whitelist``` (*weird*, I know).

## ERD
![ERD](https://github.com/philingyuup/EZStore-Server/raw/master/public/EZStore-ERD.png "EZStore API ERD")

## Instructions
Here's the instructions on how to use the EZStore-Server API

> If TOKEN REQUIRED is set to Yes, please include this in your http request:
> ```javascript
>   {
>     headers: {
>       'Authorization': `Token ${token}`
>     }
>   }
> ```

___IMPORTANT NOTE___: Django requires a trailing slash in all http requests (i.e. ```api.com/sign-in/```).

**USER**
| PURPOSE | EXTENSION | VERB | TOKEN REQUIRED | RETURN OBJECT | RETURN STATUS |
| --- | --- | --- | --- | --- | --- |
| Sign Up | '/sign-up/' | 'POST' | NO | User Object | 200 |
| Sign In | '/sign-in/' | 'POST' | NO | User Object | 200 |
| Change Password | '/change-pw/' | 'PATCH' | YES | None | 204 |
| Sign out | '/sign-out/' | 'DELETE' | YES | None | 204 |

These are the data format for the API calls

*SIGN UP*
```javascript
{
    "credentials": {
        "email": <email>,
        "password": <password>
    }
}
// password confirmation is done client side
```

*SIGN IN*
```javascript
{
  "credentials": {
    "email": <email>,
    "password": <password>
  }
}
```

*CHANGE PASSWORD*
```javascript
{
  "passwords": {
    "old": <oldPassword>,
    "new": <newPassword>
  }
}
```

**PRODUCT**
| PURPOSE | EXTENSION | VERB | TOKEN REQUIRED | RETURN OBJECT | RETURN STATUS |
| --- | --- | --- | --- | --- | --- |
| Show All | '/products/' | 'GET' | No | Array of Product Objects | 200 |
| Show One | '/products/:id/' | 'GET' | NO | Product Object | 200 |
| Create | '/products/' | 'POST' | YES | Product Object | 201 |
| Update | '/products/:id' | 'PATCH' | YES | Product Object | 200 |
| Destroy | '/products/:id' | 'DELETE' | YES | None | 204 |

These are the data format for the API calls

*CREATE*
```javascript
{
    "product": {
        "name": <name>,
        "img": <imageUrl>,
        "short_description": <text>,
        "long_description": <text>,
        "price": <float w/ two decimals>
    }
}
```

*UPDATE*
```javascript
{
    "product": {
        "name": <name>,
        "img": <imageUrl>,
        "short_description": <text>,
        "long_description": <text>,
        "price": <float w/ two decimals>
    }
}
// Partial updates are enabled so if you don't want to update a certain key, just
// omit it from the data (key and value).
// The code below will work and won't affect the keys that aren't listed.
{
    "product": {
        "long_description": <text>,
        "img": <imageUrl>,
        "price": <float w/ two decimals>
    }
}
```

**CLOUDINARY**
*NOTE*: Due to this being an unsigned preset, I won't be sharing the exact url with you.

> URL='https://api.cloudinary.com/v1_1/exampleCloudName/image/upload'

Please note that both actions are POST requests

| PURPOSE | URL | VERB | RETURN OBJECT |
| --- | --- | --- | --- |
| Upload | see above | 'POST' | Cloudinary Object |
| Delete (conditional, see below) | see above | 'POST' | None |

These are the data format for the api call

*UPLOAD*
```javascript
{
  'file': <event.target.files[0]>,
  'upload_preset': 'ezstore'
}
// Remember that event.target.files is an array and unsigned html upload through
// Cloudinary only allows single file uploads.
// The secure_url is the value to the 'img' key in our Product object.
```

*DELETE*
```javascript
{
  'token': <deleteToken>
}
// Upon a successful upload, a delete_token will be in the response object. Cloudinary
// allows unsigned html deletion on files that have just been recently updated. The
// delete_token is only valid for 10 minutes upon a successful upload.
```

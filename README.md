### To run this project on your computer you need:
+ clone this repository on your computer;
+ run migrations to create a database **(python manage.py migrate)**;
+ start server **(python manage.py runserver)**

# WeatherApp
This project gives information about the current weather in any city entered in the input line.

## Backend
The basic data for displaying the main page is processed as usual in a **"views.py"**. The entire internal part of the responses and button interactions, receiving and processing weather information and working with the database is in the backend directory.

## Site principles
### Requirements.txt
***Django*** framework is used as the backbone of the project. For API request ***requests*** module is used. To encrypt the token ***python-decouple*** is used.
A ***Jinja2*** is required to connect the backend and frontend.

### Header
The site header with pointers ***"Главная"***, ***"Информация"***, ***"Документация"*** is made only for beauty. 
Interaction with them does not break the site, but it does not transfer the user anywhere, just leaving him on the main page.

### Input line *("Погода в вашем городе")*
The input line accepts the name of the city where the user wants to know the weather. The input is not case and language sensitive.

If the input line is empty and the user is trying to find out the weather, then the process will not start and a red inscription ***"Введите город"***
will be displayed that the city must first be entered.

### Start button *("Узнать")*
This button starts the process of searching and displaying the weather. Also, this process starts with the enter keyboard button.

### Output list *("Информация")*
This list displays information about the weather in the city: temperature and cloudiness.
Regardless of the input language and case, the output of the city will be in Russian and with a capital letter.

If the user enters a city that already has information about it, then a new copy of the city is not added, but the weather information
on the already existing row is updated. The output recognizes the city entered in different languages, for example *"Москва"* equals *"Moscow"*, 
so there will be no copy of the city.

If the entered city does not exist, then a row with information about the error is displayed.

### Clear button *("Очистить")*
This button clears the list of output cities.

### Settings *("Настройки")*
+ **Single city button** - activates the **single mode**. When entering a new city, the old one is deleted and a new one is added:
> 1. If there are cities in the list, displays the last city from the list.
+ **Default city button** - activates the **default mode**. At the moment, the default city is **"Москва"**:
> 1. If the output list is empty, then the default city weather information will be added;
> 2. If there are cities in the list, but there is no default city, then it will be added to the **top** of the list;
> 3. If there is already a default city in the list, then its weather information will be updated and it will **move to the top** of the list;
> 4. When clearing the list, all cities will be deleted **except** for the default city;
> 5. When you turn the mod on and off, the default city is not deleted.
+ **Single & default** - how mods work depending on the state of another mod:
> 1. Default mode does not interfere with the work of the single mode;
> 2. If default mod is on:
>> + When you turn on a single mod, the list will not contain the last city, but the default city;
>> + If the single mod is on and the list contains a city another than the default one, then after disabling the single mod, the default city will appear in the top of the list.
> 3. If single mod is on:
>> + When you torn on default mod, the city in the list changes to the default city.

## Сurrent disadvantages
1. There is no possibility to change the default city;

2. Bug on page refresh.
+ If the last interaction was with the settings buttons, then when the page is refreshed, the last pressed settings button will change its status to the opposite.
+ If the last interaction was on an input line with a city added, then when the page is refreshed, the last added city will be added to the list again, despite the sorting function.

This bug is related to the fact that request.POST does not clear the status after the command is executed and the page is refreshed. And it turns out that when the page is refreshed, the last command is forcibly executed again, bypassing the main debugging and sorting functions.

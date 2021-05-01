# Software Requirements

## Vision
The vision of this project is to create a landscape world that allows the user to login and create and destroy blocks. These blocks can be used to build a digital world. This game allows a user to expand their creativity and kill boredom. Our first goal is to let the user expand on their creativity. Our stretch goal is to have a Survival mode that challenges the user to survive in their constructed universe (build shelter, find food, and craft tools). 

## Scope
Scope (In): The game will allow users to move and jump (arrow keys) and create/destroy blocks (mouse click). The user will be able to log in and out with user credentials. The game will save high scores and display them upon log in. 

Scope (Out): The game app will not be a mobile app. 

## MVP
Our MVP is to create a defined play area / landscape (100 x 100 blocks), create game user, login page, movements (walking, jumping), high score legend, and create/destroy blocks.  

Dependencies: three, react-three-fiber, use-cannon, zustand, drei, nanoid

Stretch goals: Survival mode that challenges the user to survive in their constructed universe (build shelter, find food, create animals, and craft tools)

## Functional Requirements
Admin: create user account 
DB: user & scores
Cache/Memory: reset landscape upon refresh (MVP), save previous landscape (stretch)
Game (User Actions): walk, jump, create/destroy block, place block 
Data Flow: User logs in from the main page, gets taken to an empty landscape, ability to move/jump around the landscape, create/destroy/place blocks, and accumulate points based on a scoring system. Reset landscape upon refresh and as a stretch goal, save the previous landscape upon log out. 

## Non-Functional Requirements
Security: Login credentials required
Usability: Use React to get game developed and displayed on web browsers (plan B: use Pygame or Pyglet with Skulpt)
Testability: Test for a minimum of 80% coverage.

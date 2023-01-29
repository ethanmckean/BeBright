# BeBright
Spartahack 8 Hackathon Project

## Inspiration
Inspired by the popular app BeReal, BeBright aims to encourage incremental studying through a short five minute question each day at a random (reasonable!) time. 

## What it does
After being invited to a class, users will receive a push notification and/or SMS when their class' question goes live. Then, they have five minutes to solve the question for extra credit. 

## How we built it
We used Flask to build our backend and React Native for the frontend. For our landing page, we used Velo by Wix. React Native allows for questions to be answered both from mobile platforms as well as the web, essential for accessibility across communities where access to technologies may be varied. 

## Challenges we ran into
While our database can handle user authentication and data storage, we ran into issues integrating a Firebase UI log in with react-native. With more time, however, integrations with Firebase, Twilio, and more are possible. Overall, our teams limited experience in frontend app development became a bottleneck.

## Accomplishments that we're proud of
Our backend successfully integrates with our cross platform front end. We also have a clean landing page with a custom domain.

## What we learned
Often times attempting to integrate various third party services introduced friction when inexplicable errors and other issues appeared. While we were quick to coming up with our idea and developing/unit testing the backend we underestimated the overhead creating a cross-platform frontend would take for first time react developers.

## What's next for BeBright
In future weekends we may choose to flush out the user experience. Additional question formats, a teacher dashboard UI, platform-specific push notifications (*cough* Apple requiring a Developer account), and more our on our TODO list. 

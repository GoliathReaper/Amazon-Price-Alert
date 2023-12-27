# Amazon Price Alert
## Introduction
Amazon Price Alert is a web application developed using Python Flask that notifies users when the price of a selected product matches the expected price set by the user.

## Features
**Price Tracking:** Users can set their desired price for a specific product on Amazon.
**Alert Notifications:** The app sends notifications when the product's price meets the user-defined threshold.
**User-Friendly Interface:** Simple and intuitive interface for easy interaction.

## Technologies Used
* **Python Flask:** Backend development framework.
* **HTML/CSS:** Frontend design and structure.
* **Docker:** Containerization for easy deployment.

## Usage

### Telegram Notification setup

#### Creating a New Bot in Telegram
1. Open Telegram and search for BotFather.
2. Start a chat with BotFather.
3. Use the /newbot command and follow the prompts to create a new bot.
4. Once created, you'll receive a telegram_token for your bot.


#### Creating a New Group in Telegram
1. Open Telegram and tap on the hamburger menu (three horizontal lines).
2. Select "New Group" and follow the instructions to create a new group.
3. Name the group as "Amazon Price Alert" or a desired name.
4. Invite your created bot to the group.

#### Managing Environment Variables
1. Create a .env file in the project directory.
2. Add the necessary environment variables to the .env file:

```env
my_mail_id=your_email@example.com
mail_password=your_email_password
telegram_token=your_telegram_bot_token
telegram_chat_id=your_telegram_chat_id
```
Replace the placeholder values **(your_email@example.com, your_email_password, your_telegram_bot_token, your_telegram_chat_id)** with your actual credentials and tokens.

### Local Deployment
To run the application locally:

1. Clone the repository:

```cmd
git clone https://github.com/your-username/amazon-price-alert.git
```

2. Navigate to the project directory:

```cmd
cd amazon-price-alert
```

3. Install dependencies:

```cmd
pip install -r requirements.txt
```

4. Run the application:

```cmd
python app.py
```
5. Access the app in a web browser:

   Open a browser and go to http://localhost:5000.

### Docker Deployment

To deploy using Docker:

1. Build the Docker image:

```cmd
docker build -t amazon-price-alert .
```

2. Run the Docker container:

```cmd
docker run -p 5000:5000 amazon-price-alert
```

3. Access the app in a web browser:

   Open a browser and go to http://localhost:5000.

## Directory Structure
* **app.py:** Main Flask application file.
* **templates:** Contains HTML templates for rendering web pages.
**static:** Includes CSS files for styling.
**Dockerfile:** Instructions for building the Docker image.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

### License

This project is licensed under the MIT License.


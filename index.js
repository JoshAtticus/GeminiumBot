const dotenv = require('dotenv');
const axios = require('axios').default;

dotenv.config();

async function startBot() {
    const Bot = await import("meowerbot");
    const bot = new Bot.default();

    bot.onLogin(() => {
        console.log("Bot has logged in!");
    });

    bot.onCommand("help", (ctx) => {
        ctx.reply("Commands: @Geminium help");
    });

    bot.onCommand("ask", (ctx) => {
        const question = ctx.args.slice(1).join(" "); // remove the command itself
    
        var options = {
            method: 'POST',
            url: 'https://geminium.joshatticus.online/api/geminium/ask',
            headers: {'Content-Type': 'application/json'},
            data: {question: question}
        };
      
        axios.request(options).then(function (response) {
            ctx.reply(response.data);
        }).catch(function (error) {
            console.error(error);
        });
    });    

    bot.onCommand((command, ctx) => {
        ctx.reply(`That command doesn't exist! Send @Geminium help for a list of commands`);
    });

    bot.onMessage((data) => {
        console.log(`New message: ${data}`);
    });

    bot.onClose(() => {
        console.log("Disconnected");
        bot.login(process.env.GBOT_USERNAME, process.env.GBOT_PASSWORD);
    });

    bot.login(process.env.GBOT_USERNAME, process.env.GBOT_PASSWORD);
}

startBot();

const qrcode = require('qrcode-terminal');
const { Client } = require('whatsapp-web.js');

const client = new Client();

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('WhatsApp Web client is ready!');
    const number = '9385357001'; // Customer's number
    const message = 'Your daily service status: All services are operational.';
    const chatId = `${number}@c.us`;

    client.sendMessage(chatId, message).then(response => {
        console.log('Message sent:', response);
    }).catch(err => {
        console.error('Error sending message:', err);
    });
});

client.initialize();

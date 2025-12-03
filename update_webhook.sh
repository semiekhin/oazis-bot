#!/bin/bash
sleep 10
TUNNEL_URL=$(journalctl -u cloudflared-oazis -n 50 --no-pager | grep -o 'https://[a-z-]*\.trycloudflare\.com' | tail -1)
if [ -n "$TUNNEL_URL" ]; then
    curl -s "https://api.telegram.org/bot8045360544:AAGDk-Ti0j_wfoatxZYKAADg7F_Eqv53w2A/setWebhook?url=${TUNNEL_URL}/telegram/webhook"
    echo "$(date): Oazis webhook updated to: $TUNNEL_URL" >> /var/log/oazis-webhook.log
fi

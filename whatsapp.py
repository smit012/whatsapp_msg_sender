# whatsapp_sender_app.py

import streamlit as st
import pywhatkit as kit
import random
import time
import datetime

st.set_page_config(page_title="Safe WhatsApp Sender", layout="centered")

st.title("📱 Safe WhatsApp Sender (2–3 Min Gap)")

st.markdown("""
This app sends random messages to WhatsApp contacts with **2–3 minute gaps** to avoid spam detection.

⚠️ **IMPORTANT:**
- Use only with **your contacts**
- Numbers must be in international format (e.g., `+919876543210`)
- WhatsApp Web must be logged in on your default browser
""")

# Input area
messages_input = st.text_area("✍️ Enter multiple message variations (one per line):")
numbers_input = st.text_area("📱 Enter phone numbers (one per line, with country code):")

start_button = st.button("🚀 Start Sending Messages")

if start_button:
    if not messages_input.strip() or not numbers_input.strip():
        st.error("⚠️ Please fill both message and phone number fields.")
    else:
        messages = [msg.strip() for msg in messages_input.strip().split('\n') if msg.strip()]
        numbers = [num.strip() for num in numbers_input.strip().split('\n') if num.strip()]
        
        if not messages:
            st.error("No messages found.")
        elif not numbers:
            st.error("No phone numbers found.")
        else:
            st.success(f"✅ Starting to send messages to {len(numbers)} numbers.")
            st.warning("⏳ Keep the browser open and do not interrupt the sending process.")

            sent_count = 0
            fail_count = 0

            log_placeholder = st.empty()

            for i, number in enumerate(numbers):
                selected_msg = random.choice(messages)
                now = datetime.datetime.now()
                send_hour = now.hour
                send_minute = now.minute + 1

                if send_minute >= 60:
                    send_hour += 1
                    send_minute -= 60

                log_placeholder.markdown(f"📤 Sending to `{number}` → `{selected_msg}`")

                try:
                    # Send message
                    kit.sendwhatmsg(
                        phone_no=number,
                        message=selected_msg,
                        time_hour=send_hour,
                        time_min=send_minute,
                        wait_time=10,
                        tab_close=True
                    )

                    sent_count += 1
                    st.success(f"✅ Message sent to {number} at {send_hour}:{send_minute:02d}")
                except Exception as e:
                    fail_count += 1
                    st.error(f"❌ Failed to send to {number}: {str(e)}")

                if i < len(numbers) - 1:
                    delay = random.randint(120, 180)
                    st.info(f"⏱ Waiting for {delay} seconds before sending next message...")
                    time.sleep(delay)

            st.balloons()
            st.success(f"🎯 Completed. Sent: {sent_count}, Failed: {fail_count}")
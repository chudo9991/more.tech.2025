#!/usr/bin/env python3
"""
SIP Provider Simulator for testing webhooks
"""
import asyncio
import aiohttp
import json
import uuid
import time
from typing import Dict, Any


class SIPSimulator:
    def __init__(self, orchestrator_url: str = "http://localhost:8000"):
        self.orchestrator_url = orchestrator_url
        self.session_id = None

    async def simulate_call_flow(self):
        """Simulate complete call flow"""
        print("🚀 Starting SIP call simulation...")
        
        # Step 1: Call start
        await self.simulate_call_start()
        await asyncio.sleep(1)
        
        # Step 2: Call answered
        await self.simulate_call_answered()
        await asyncio.sleep(2)
        
        # Step 3: Record ready (answer audio)
        await self.simulate_record_ready()
        await asyncio.sleep(1)
        
        # Step 4: Call end
        await self.simulate_call_end()
        
        print("✅ Call simulation completed!")

    async def simulate_call_start(self):
        """Simulate call start event"""
        event_data = {
            "event": "call_start",
            "call_id": f"CALL_{uuid.uuid4().hex[:8].upper()}",
            "phone": "+7-999-123-45-67",
            "timestamp": int(time.time()),
            "request_id": str(uuid.uuid4())
        }
        
        print(f"📞 Call start: {event_data['call_id']}")
        await self._send_webhook("/api/v1/webhooks/call", event_data)

    async def simulate_call_answered(self):
        """Simulate call answered event"""
        event_data = {
            "event": "call_answer",
            "call_id": f"CALL_{uuid.uuid4().hex[:8].upper()}",
            "timestamp": int(time.time()),
            "request_id": str(uuid.uuid4())
        }
        
        print(f"📱 Call answered: {event_data['call_id']}")
        await self._send_webhook("/api/v1/webhooks/call", event_data)

    async def simulate_record_ready(self):
        """Simulate recording ready event"""
        event_data = {
            "event": "record_ready",
            "call_id": f"CALL_{uuid.uuid4().hex[:8].upper()}",
            "record_url": "https://minio:9000/interview-audio/answer_001.wav",
            "duration_ms": 15000,
            "file_size_bytes": 240000,
            "timestamp": int(time.time()),
            "request_id": str(uuid.uuid4())
        }
        
        print(f"🎙️ Record ready: {event_data['record_url']}")
        await self._send_webhook("/api/v1/webhooks/record", event_data)

    async def simulate_call_end(self):
        """Simulate call end event"""
        event_data = {
            "event": "call_end",
            "call_id": f"CALL_{uuid.uuid4().hex[:8].upper()}",
            "duration_ms": 45000,
            "timestamp": int(time.time()),
            "request_id": str(uuid.uuid4())
        }
        
        print(f"📴 Call end: {event_data['call_id']}")
        await self._send_webhook("/api/v1/webhooks/call", event_data)

    async def _send_webhook(self, endpoint: str, data: Dict[str, Any]):
        """Send webhook to orchestrator"""
        url = f"{self.orchestrator_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "X-Request-ID": data.get("request_id", str(uuid.uuid4())),
            "User-Agent": "SIP-Simulator/1.0"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, headers=headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(f"✅ Webhook sent successfully: {result}")
                    else:
                        print(f"❌ Webhook failed: {response.status} - {await response.text()}")
        except Exception as e:
            print(f"❌ Webhook error: {e}")

    async def simulate_full_interview(self):
        """Simulate a complete interview session"""
        print("🎯 Starting full interview simulation...")
        
        # Create session
        session_data = {
            "vacancy_id": "SWE_BACK_001",
            "phone": "+7-999-123-45-67",
            "email": "test@example.com"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Create session
                async with session.post(
                    f"{self.orchestrator_url}/api/v1/sessions/",
                    json=session_data
                ) as response:
                    if response.status == 200:
                        session_result = await response.json()
                        self.session_id = session_result["id"]
                        print(f"📋 Session created: {self.session_id}")
                    else:
                        print(f"❌ Session creation failed: {response.status}")
                        return

                # Simulate questions and answers
                for step in range(1, 4):  # Simulate 3 questions
                    print(f"\n❓ Question {step}:")
                    
                    # Get next question
                    async with session.post(
                        f"{self.orchestrator_url}/api/v1/sessions/{self.session_id}/next"
                    ) as response:
                        if response.status == 200:
                            question = await response.json()
                            print(f"   Question: {question['question_text'][:50]}...")
                        else:
                            print(f"   ❌ Failed to get question: {response.status}")
                            continue

                    # Simulate answer
                    answer_data = {
                        "question_id": question["question_id"],
                        "audio_url": f"https://minio:9000/interview-audio/answer_{step:03d}.wav"
                    }
                    
                    async with session.post(
                        f"{self.orchestrator_url}/api/v1/sessions/{self.session_id}/answer",
                        json=answer_data
                    ) as response:
                        if response.status == 200:
                            answer_result = await response.json()
                            print(f"   ✅ Answer submitted: {answer_result['status']}")
                        else:
                            print(f"   ❌ Answer submission failed: {response.status}")

                    await asyncio.sleep(1)

                # Get final session status
                async with session.get(
                    f"{self.orchestrator_url}/api/v1/sessions/{self.session_id}"
                ) as response:
                    if response.status == 200:
                        final_session = await response.json()
                        print(f"\n📊 Final session status: {final_session['status']}")
                        print(f"   Total score: {final_session.get('total_score', 'N/A')}")
                    else:
                        print(f"❌ Failed to get session status: {response.status}")

        except Exception as e:
            print(f"❌ Interview simulation error: {e}")


async def main():
    """Main function"""
    import sys
    
    orchestrator_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    simulation_type = sys.argv[2] if len(sys.argv) > 2 else "call"
    
    simulator = SIPSimulator(orchestrator_url)
    
    if simulation_type == "call":
        await simulator.simulate_call_flow()
    elif simulation_type == "interview":
        await simulator.simulate_full_interview()
    else:
        print("Usage: python sip_simulator.py [orchestrator_url] [call|interview]")
        print("  call: Simulate basic call flow")
        print("  interview: Simulate complete interview session")


if __name__ == "__main__":
    asyncio.run(main())

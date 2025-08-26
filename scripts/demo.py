#!/usr/bin/env python3
"""
Demo script for testing the complete interview system
"""
import asyncio
import aiohttp
import json
import time
from datetime import datetime
from typing import Dict, Any


class InterviewDemo:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session_id = None
        self.results = {}

    async def run_full_demo(self):
        """Run complete demo from start to finish"""
        print("🚀 Starting Interview AI Demo")
        print("=" * 50)
        
        try:
            # Step 1: Create session
            await self.create_session()
            
            # Step 2: Simulate interview questions
            await self.simulate_interview()
            
            # Step 3: Get final results
            await self.get_final_results()
            
            # Step 4: Export reports
            await self.export_reports()
            
            # Step 5: Check monitoring
            await self.check_monitoring()
            
            print("\n✅ Demo completed successfully!")
            self.print_summary()
            
        except Exception as e:
            print(f"\n❌ Demo failed: {e}")
            raise

    async def create_session(self):
        """Create a new interview session"""
        print("\n📋 Step 1: Creating interview session...")
        
        session_data = {
            "vacancy_id": "SWE_BACK_001",
            "phone": "+7-999-123-45-67",
            "email": "demo@example.com"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/api/v1/sessions/",
                json=session_data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    self.session_id = result["id"]
                    print(f"   ✅ Session created: {self.session_id}")
                    print(f"   📊 Total steps: {result['total_steps']}")
                else:
                    raise Exception(f"Failed to create session: {response.status}")

    async def simulate_interview(self):
        """Simulate interview questions and answers"""
        print("\n🎤 Step 2: Simulating interview...")
        
        questions_answered = 0
        max_questions = 3  # Limit for demo
        
        async with aiohttp.ClientSession() as session:
            while questions_answered < max_questions:
                # Get next question
                async with session.post(
                    f"{self.base_url}/api/v1/sessions/{self.session_id}/next"
                ) as response:
                    if response.status == 200:
                        question_data = await response.json()
                        print(f"\n   ❓ Question {questions_answered + 1}: {question_data['question_text'][:50]}...")
                        
                        # Simulate answer
                        answer_data = {
                            "question_id": question_data["question_id"],
                            "audio_url": f"https://minio:9000/interview-audio/demo_answer_{questions_answered + 1:03d}.wav"
                        }
                        
                        async with session.post(
                            f"{self.base_url}/api/v1/sessions/{self.session_id}/answer",
                            json=answer_data
                        ) as response:
                            if response.status == 200:
                                answer_result = await response.json()
                                print(f"   ✅ Answer submitted successfully")
                                print(f"   📈 Progress: {answer_result['session_progress']['current_step']}/{answer_result['session_progress']['total_steps']}")
                                
                                if answer_result['session_progress']['status'] == 'completed':
                                    print("   🎉 Interview completed!")
                                    break
                            else:
                                print(f"   ❌ Failed to submit answer: {response.status}")
                                break
                        
                        questions_answered += 1
                        await asyncio.sleep(1)  # Small delay between questions
                    else:
                        print(f"   ❌ Failed to get next question: {response.status}")
                        break

    async def get_final_results(self):
        """Get final session results"""
        print("\n📊 Step 3: Getting final results...")
        
        async with aiohttp.ClientSession() as session:
            # Get session details
            async with session.get(
                f"{self.base_url}/api/v1/sessions/{self.session_id}"
            ) as response:
                if response.status == 200:
                    session_data = await response.json()
                    print(f"   📋 Session status: {session_data['status']}")
                    print(f"   🎯 Total score: {(session_data.get('total_score', 0) * 100):.1f}%")
                    print(f"   ✅ Pass rate: {(session_data.get('pass_rate', 0) * 100):.1f}%")
                    
                    # Get detailed results
                    async with session.get(
                        f"{self.base_url}/api/v1/sessions/{self.session_id}/results"
                    ) as response:
                        if response.status == 200:
                            results = await response.json()
                            self.results = results
                            print(f"   📝 Questions answered: {results['answered_questions']}")
                            print(f"   ⏱️  Completion rate: {(results['completion_rate'] * 100):.1f}%")

    async def export_reports(self):
        """Export various report formats"""
        print("\n📄 Step 4: Exporting reports...")
        
        formats = ["json", "csv", "pdf", "html"]
        
        async with aiohttp.ClientSession() as session:
            for format in formats:
                try:
                    async with session.get(
                        f"{self.base_url}/api/v1/hr/sessions/{self.session_id}/export",
                        params={"format": format}
                    ) as response:
                        if response.status == 200:
                            export_data = await response.json()
                            print(f"   ✅ {format.upper()} report exported: {export_data['filename']}")
                        else:
                            print(f"   ⚠️  {format.upper()} export failed: {response.status}")
                except Exception as e:
                    print(f"   ❌ {format.upper()} export error: {e}")

    async def check_monitoring(self):
        """Check system monitoring"""
        print("\n🔍 Step 5: Checking system monitoring...")
        
        async with aiohttp.ClientSession() as session:
            # Check system health
            async with session.get(
                f"{self.base_url}/api/v1/monitoring/health"
            ) as response:
                if response.status == 200:
                    health_data = await response.json()
                    print(f"   🏥 System status: {health_data['status']}")
                    print(f"   🗄️  Database: {health_data['database']['status']}")
                else:
                    print(f"   ❌ Health check failed: {response.status}")
            
            # Get session metrics
            async with session.get(
                f"{self.base_url}/api/v1/monitoring/metrics/sessions",
                params={"time_range": "24h"}
            ) as response:
                if response.status == 200:
                    metrics = await response.json()
                    print(f"   📈 Total sessions (24h): {metrics['total_sessions']}")
                    print(f"   ✅ Completion rate: {(metrics['completion_rate'] * 100):.1f}%")
                    print(f"   ⏱️  Avg completion time: {metrics['avg_completion_time_minutes']:.1f} min")

    def print_summary(self):
        """Print demo summary"""
        print("\n" + "=" * 50)
        print("📋 DEMO SUMMARY")
        print("=" * 50)
        
        if self.results:
            print(f"Session ID: {self.results['session_id']}")
            print(f"Status: {self.results['status']}")
            print(f"Questions: {self.results['answered_questions']}/{self.results['total_questions']}")
            print(f"Completion Rate: {(self.results['completion_rate'] * 100):.1f}%")
            print(f"Total Score: {(self.results['total_score'] * 100):.1f}%")
            print(f"Pass Rate: {(self.results['pass_rate'] * 100):.1f}%")
        
        print(f"\n🌐 Frontend: http://localhost:3000")
        print(f"📚 API Docs: http://localhost:8000/docs")
        print(f"📊 MinIO Console: http://localhost:9001")
        print(f"🗄️  Database: localhost:5432")

    async def test_individual_services(self):
        """Test individual services"""
        print("\n🔧 Testing individual services...")
        
        services = [
            ("Orchestrator", f"{self.base_url}/healthz"),
            ("STT", "http://localhost:8001/healthz"),
            ("TTS", "http://localhost:8002/healthz"),
            ("Scoring", "http://localhost:8003/healthz"),
        ]
        
        async with aiohttp.ClientSession() as session:
            for service_name, url in services:
                try:
                    async with session.get(url) as response:
                        if response.status == 200:
                            print(f"   ✅ {service_name}: Healthy")
                        else:
                            print(f"   ❌ {service_name}: Unhealthy ({response.status})")
                except Exception as e:
                    print(f"   ❌ {service_name}: Error - {e}")


async def main():
    """Main function"""
    import sys
    
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    demo = InterviewDemo(base_url)
    
    # Test individual services first
    await demo.test_individual_services()
    
    # Run full demo
    await demo.run_full_demo()


if __name__ == "__main__":
    asyncio.run(main())

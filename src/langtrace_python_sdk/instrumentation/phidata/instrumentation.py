"""
Copyright (c) 2025 Scale3 Labs

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from typing import Collection

from importlib_metadata import version as v
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import get_tracer
from wrapt import wrap_function_wrapper as _W

from .patch import patch_agent, patch_memory


class PhiDataInstrumentation(BaseInstrumentor):
    def instrumentation_dependencies(self) -> Collection[str]:
        return ["phidata >= 2.7.10"]  # Adjust version as needed

    def _instrument(self, **kwargs):
        tracer_provider = kwargs.get("tracer_provider")
        tracer = get_tracer(__name__, "", tracer_provider)
        version = v("phidata")

        try:
            _W(
                "phi.agent.agent",
                "Agent.run",
                patch_agent("Agent.run", version, tracer),
            )
            _W(
                "phi.agent.agent",
                "Agent.arun",
                patch_agent("Agent.arun", version, tracer),
            )
            _W(
                "phi.agent.agent",
                "Agent._run",
                patch_agent("Agent._run", version, tracer),
            )
            _W(
                "phi.agent.agent", 
                "Agent._arun",
                patch_agent("Agent._arun", version, tracer),
            )

            _W(
                "phi.memory.agent",
                "AgentMemory.update_memory",
                patch_memory("AgentMemory.update_memory", version, tracer),
            )
            _W(
                "phi.memory.agent",
                "AgentMemory.aupdate_memory",
                patch_memory("AgentMemory.aupdate_memory", version, tracer),
            )
            _W(
                "phi.memory.agent",
                "AgentMemory.update_summary",
                patch_memory("AgentMemory.update_summary", version, tracer),
            )
            _W(
                "phi.memory.agent",
                "AgentMemory.aupdate_summary",
                patch_memory("AgentMemory.aupdate_summary", version, tracer),
            )

        except Exception:
            pass

    def _uninstrument(self, **kwargs):
        pass
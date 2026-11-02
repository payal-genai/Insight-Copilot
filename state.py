from typing import TypedDict, List, Any, Optional


class InsightState(TypedDict):

    question: str
    
    conversation_history: List[Any]

    plan: str

    selected_tools: List[str]

    group_by: Optional[str]

    metric: Optional[str]

    operation: Optional[str]

    tool_results: List[Any]

    final_answer: str
"""
Event Queue Simulator with Priority Queue (Min-Heap)
Simulates time-based event processing with priorities
"""

import heapq
from typing import List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass(order=True)
class Event:
    """
    Event class for priority queue
    Events are ordered by time, then by priority
    """
    time: float
    priority: int = field(compare=True)
    event_id: int = field(compare=False)
    description: str = field(compare=False)
    data: dict = field(default_factory=dict, compare=False)
    
    def __str__(self):
        return f"Event(id={self.event_id}, time={self.time}, priority={self.priority}, desc='{self.description}')"
    
    def __repr__(self):
        return self.__str__()


class EventQueue:
    """
    Priority queue-based event simulator using min-heap
    """
    
    def __init__(self):
        """Initialize empty event queue"""
        self.heap = []
        self.current_time = 0.0
        self.next_event_id = 1
        self.processed_events = []
        self.event_history = []
    
    def add_event(self, time: float, priority: int, description: str, data: dict = None) -> Event:
        """
        Add a new event to the queue
        
        Args:
            time: Time when event should occur
            priority: Event priority (lower = higher priority)
            description: Event description
            data: Optional additional data
            
        Returns:
            Created Event object
        """
        if time < self.current_time:
            raise ValueError(f"Cannot add event in the past (current time: {self.current_time}, event time: {time})")
        
        event = Event(
            time=time,
            priority=priority,
            event_id=self.next_event_id,
            description=description,
            data=data or {}
        )
        
        heapq.heappush(self.heap, event)
        self.next_event_id += 1
        self.event_history.append(('added', event, self.current_time))
        
        return event
    
    def process_next_event(self) -> Optional[Event]:
        """
        Process the next event in the queue
        
        Returns:
            Processed Event object, or None if queue is empty
        """
        if not self.heap:
            return None
        
        event = heapq.heappop(self.heap)
        
        # Advance time to event time
        self.current_time = event.time
        
        # Record processing
        self.processed_events.append(event)
        self.event_history.append(('processed', event, self.current_time))
        
        return event
    
    def peek_next_event(self) -> Optional[Event]:
        """
        View the next event without processing it
        
        Returns:
            Next Event object, or None if queue is empty
        """
        return self.heap[0] if self.heap else None
    
    def process_until_time(self, target_time: float) -> List[Event]:
        """
        Process all events up to a specific time
        
        Args:
            target_time: Process events until this time
            
        Returns:
            List of processed events
        """
        processed = []
        
        while self.heap and self.heap[0].time <= target_time:
            event = self.process_next_event()
            if event:
                processed.append(event)
        
        # Advance time even if no events processed
        if target_time > self.current_time:
            self.current_time = target_time
        
        return processed
    
    def process_n_events(self, n: int) -> List[Event]:
        """
        Process the next n events
        
        Args:
            n: Number of events to process
            
        Returns:
            List of processed events
        """
        processed = []
        
        for _ in range(min(n, len(self.heap))):
            event = self.process_next_event()
            if event:
                processed.append(event)
        
        return processed
    
    def get_pending_events(self) -> List[Event]:
        """
        Get all pending events (sorted by priority)
        
        Returns:
            List of pending events
        """
        return sorted(self.heap)
    
    def size(self) -> int:
        """
        Get number of pending events
        
        Returns:
            Number of events in queue
        """
        return len(self.heap)
    
    def is_empty(self) -> bool:
        """
        Check if queue is empty
        
        Returns:
            True if no pending events
        """
        return len(self.heap) == 0
    
    def clear(self):
        """Clear all pending events"""
        self.heap = []
        self.event_history.append(('cleared', None, self.current_time))
    
    def reset(self):
        """Reset the entire simulator"""
        self.heap = []
        self.current_time = 0.0
        self.next_event_id = 1
        self.processed_events = []
        self.event_history = []
    
    def get_current_time(self) -> float:
        """Get current simulation time"""
        return self.current_time
    
    def get_processed_events(self) -> List[Event]:
        """Get list of all processed events"""
        return self.processed_events.copy()
    
    def get_statistics(self) -> dict:
        """
        Get statistics about the event queue
        
        Returns:
            Dictionary with statistics
        """
        return {
            'current_time': self.current_time,
            'pending_events': len(self.heap),
            'processed_events': len(self.processed_events),
            'total_events': self.next_event_id - 1,
            'next_event_time': self.heap[0].time if self.heap else None
        }
    
    def __len__(self):
        """Support len() function"""
        return len(self.heap)
    
    def __str__(self):
        return f"EventQueue(time={self.current_time}, pending={len(self.heap)}, processed={len(self.processed_events)})"


class EventSimulator:
    """
    Higher-level event simulator with common event types
    """
    
    # Common event types
    EVENT_TYPES = {
        'TASK_START': 1,
        'TASK_END': 2,
        'DEADLINE': 3,
        'MEETING': 4,
        'ALERT': 5,
        'MAINTENANCE': 6,
        'BACKUP': 7,
        'NOTIFICATION': 8
    }
    
    def __init__(self):
        """Initialize event simulator"""
        self.queue = EventQueue()
    
    def schedule_task(self, start_time: float, duration: float, task_name: str, priority: int = 5):
        """
        Schedule a task with start and end events
        
        Args:
            start_time: When task starts
            duration: How long task takes
            task_name: Task name
            priority: Task priority
        """
        # Schedule start
        self.queue.add_event(
            time=start_time,
            priority=priority,
            description=f"Start: {task_name}",
            data={'type': 'TASK_START', 'task': task_name, 'duration': duration}
        )
        
        # Schedule end
        self.queue.add_event(
            time=start_time + duration,
            priority=priority,
            description=f"End: {task_name}",
            data={'type': 'TASK_END', 'task': task_name}
        )
    
    def schedule_meeting(self, time: float, duration: float, meeting_name: str, priority: int = 3):
        """Schedule a meeting event"""
        self.queue.add_event(
            time=time,
            priority=priority,
            description=f"Meeting: {meeting_name}",
            data={'type': 'MEETING', 'duration': duration}
        )
    
    def schedule_deadline(self, time: float, deadline_name: str, priority: int = 1):
        """Schedule a high-priority deadline"""
        self.queue.add_event(
            time=time,
            priority=priority,
            description=f"DEADLINE: {deadline_name}",
            data={'type': 'DEADLINE'}
        )
    
    def schedule_recurring(self, start_time: float, interval: float, count: int, 
                          event_name: str, priority: int = 5):
        """
        Schedule recurring events
        
        Args:
            start_time: First event time
            interval: Time between events
            count: Number of occurrences
            event_name: Event description
            priority: Event priority
        """
        for i in range(count):
            event_time = start_time + (i * interval)
            self.queue.add_event(
                time=event_time,
                priority=priority,
                description=f"{event_name} #{i+1}",
                data={'type': 'RECURRING', 'occurrence': i+1}
            )
    
    def get_queue(self) -> EventQueue:
        """Get the underlying event queue"""
        return self.queue
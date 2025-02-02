import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ActiveWorkout, ExerciseLog

class WorkoutConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.workout_group_name = None
        self.workout_id = None

    async def connect(self):
        self.workout_id = self.scope['url_route']['kwargs']['workout_id']
        self.workout_group_name = f'workout_{self.workout_id}'

        await self.channel_layer.group_add(
            self.workout_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.workout_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        
        if message_type == 'exercise_complete':
            exercise_id = text_data_json.get('exercise_id')
            completed_sets = text_data_json.get('completed_sets')
            completed_reps = text_data_json.get('completed_reps')
            
            await self.update_exercise_log(
                exercise_id, completed_sets, completed_reps
            )
            
            await self.channel_layer.group_send(
                self.workout_group_name,
                {
                    'type': 'workout_update',
                    'message': {
                        'exercise_id': exercise_id,
                        'completed_sets': completed_sets,
                        'completed_reps': completed_reps
                    }
                }
            )

    async def workout_update(self, event):
        message = event['message']
        
        await self.send(text_data=json.dumps({
            'type': 'workout_update',
            'message': message
        }))

    @database_sync_to_async
    def update_exercise_log(self, exercise_id, completed_sets, completed_reps):
        workout = ActiveWorkout.objects.get(id=self.workout_id)
        ExerciseLog.objects.create(
            active_workout=workout,
            workout_exercise_id=exercise_id,
            completed_sets=completed_sets,
            completed_reps=completed_reps
        )

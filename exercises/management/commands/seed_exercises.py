from django.core.management.base import BaseCommand
from exercises.models import Exercise


class Command(BaseCommand):
    help = 'Seed the database with initial exercises'

    def handle(self, *args, **kwargs):
        exercises = [
            {
                'name': 'Push-ups',
                'description': 'A classic bodyweight exercise that targets the chest, shoulders, and triceps.',
                'instructions': '1. Start in a plank position\n2. Lower your body until your chest nearly touches the ground\n3. Push back up to the starting position',
                'target_muscles': 'Chest, Shoulders, Triceps',
                'equipment_required': 'None',
                'difficulty_level': 'beginner',
                'exercise_type': 'strength'
            },
            {
                'name': 'Squats',
                'description': 'A fundamental lower body exercise that builds strength and muscle.',
                'instructions': '1. Stand with feet shoulder-width apart\n2. Lower your body as if sitting back into a chair\n3. Keep your chest up and back straight\n4. Return to starting position',
                'target_muscles': 'Quadriceps, Hamstrings, Glutes',
                'equipment_required': 'None',
                'difficulty_level': 'beginner',
                'exercise_type': 'strength'
            },
            {
                'name': 'Deadlifts',
                'description': 'A compound exercise that targets multiple muscle groups.',
                'instructions': '1. Stand with feet hip-width apart\n2. Bend at hips and knees to grasp the bar\n3. Keep back straight and lift by extending hips and knees\n4. Return weight to ground with controlled movement',
                'target_muscles': 'Lower Back, Hamstrings, Glutes, Core',
                'equipment_required': 'Barbell, Weight Plates',
                'difficulty_level': 'intermediate',
                'exercise_type': 'strength'
            },
            {
                'name': 'Bench Press',
                'description': 'Classic chest exercise for building upper body strength.',
                'instructions': '1. Lie on bench with feet flat on ground\n2. Grip bar slightly wider than shoulder width\n3. Lower bar to chest\n4. Press bar back up to starting position',
                'target_muscles': 'Chest, Shoulders, Triceps',
                'equipment_required': 'Bench, Barbell, Weight Plates',
                'difficulty_level': 'intermediate',
                'exercise_type': 'strength'
            },
            {
                'name': 'Running',
                'description': 'Fundamental cardio exercise for improving endurance.',
                'instructions': '1. Start with proper warm-up\n2. Maintain good posture\n3. Land midfoot\n4. Keep steady breathing rhythm',
                'target_muscles': 'Legs, Core, Cardiovascular System',
                'equipment_required': 'Running Shoes',
                'difficulty_level': 'beginner',
                'exercise_type': 'cardio'
            },
            {
                'name': 'Jumping Rope',
                'description': 'High-intensity cardio that improves coordination.',
                'instructions': '1. Hold handles with relaxed grip\n2. Keep elbows close to sides\n3. Jump on balls of feet\n4. Make small jumps',
                'target_muscles': 'Calves, Shoulders, Core',
                'equipment_required': 'Jump Rope',
                'difficulty_level': 'beginner',
                'exercise_type': 'cardio'
            },
            {
                'name': 'Plank',
                'description': 'Isometric core exercise that improves stability.',
                'instructions': '1. Start in forearm plank position\n2. Keep body in straight line\n3. Engage core\n4. Hold position',
                'target_muscles': 'Core, Shoulders',
                'equipment_required': 'None',
                'difficulty_level': 'beginner',
                'exercise_type': 'strength'
            },
            {
                'name': 'Russian Twists',
                'description': 'Core exercise targeting obliques.',
                'instructions': '1. Sit with knees bent\n2. Lean back slightly\n3. Lift feet off ground\n4. Rotate torso side to side',
                'target_muscles': 'Obliques, Core',
                'equipment_required': 'Optional: Weight',
                'difficulty_level': 'intermediate',
                'exercise_type': 'strength'
            },
            {
                'name': 'Pull-ups',
                'description': 'Advanced upper body exercise for back and arms.',
                'instructions': '1. Grip bar with hands wider than shoulders\n2. Hang with arms fully extended\n3. Pull up until chin over bar\n4. Lower with control',
                'target_muscles': 'Back, Biceps, Shoulders',
                'equipment_required': 'Pull-up Bar',
                'difficulty_level': 'advanced',
                'exercise_type': 'strength'
            },
            {
                'name': 'Dips',
                'description': 'Upper body exercise for chest and triceps.',
                'instructions': '1. Support body on parallel bars\n2. Lower body by bending arms\n3. Push back up to start\n4. Keep slight forward lean',
                'target_muscles': 'Chest, Triceps, Shoulders',
                'equipment_required': 'Parallel Bars or Dip Station',
                'difficulty_level': 'intermediate',
                'exercise_type': 'strength'
            },
            {
                'name': 'Lunges',
                'description': 'Unilateral leg exercise for strength and balance.',
                'instructions': '1. Stand with feet together\n2. Step forward with one leg\n3. Lower back knee toward ground\n4. Push back to start',
                'target_muscles': 'Quadriceps, Hamstrings, Glutes',
                'equipment_required': 'None',
                'difficulty_level': 'beginner',
                'exercise_type': 'strength'
            },
            {
                'name': 'Calf Raises',
                'description': 'Isolation exercise for calf muscles.',
                'instructions': '1. Stand on edge of step\n2. Lower heels below platform\n3. Rise up on toes\n4. Lower with control',
                'target_muscles': 'Calves',
                'equipment_required': 'Step or Platform',
                'difficulty_level': 'beginner',
                'exercise_type': 'strength'
            },
            {
                'name': 'Yoga Sun Salutation',
                'description': 'Flowing sequence of yoga poses.',
                'instructions': '1. Start in mountain pose\n2. Flow through sequence\n3. Maintain breathing rhythm\n4. Move with control',
                'target_muscles': 'Full Body',
                'equipment_required': 'Yoga Mat',
                'difficulty_level': 'beginner',
                'exercise_type': 'flexibility'
            },
            {
                'name': 'Dynamic Stretching',
                'description': 'Active stretching routine for warm-up.',
                'instructions': '1. Start with light movements\n2. Gradually increase range\n3. Keep movements controlled\n4. Don\'t bounce',
                'target_muscles': 'Full Body',
                'equipment_required': 'None',
                'difficulty_level': 'beginner',
                'exercise_type': 'flexibility'
            },
            {
                'name': 'Clean and Jerk',
                'description': 'Olympic weightlifting movement.',
                'instructions': '1. Start with barbell on ground\n2. Explosively pull to shoulders\n3. Drive overhead\n4. Return to ground with control',
                'target_muscles': 'Full Body',
                'equipment_required': 'Barbell, Weight Plates',
                'difficulty_level': 'advanced',
                'exercise_type': 'strength'
            },
            {
                'name': 'Muscle-ups',
                'description': 'Advanced calisthenics movement.',
                'instructions': '1. Start with pull-up\n2. Explosively pull to transition\n3. Push to straight arms\n4. Lower with control',
                'target_muscles': 'Back, Chest, Shoulders, Arms',
                'equipment_required': 'Pull-up Bar',
                'difficulty_level': 'advanced',
                'exercise_type': 'strength'
            },
            {
                'name': 'Burpees',
                'description': 'High-intensity full body exercise.',
                'instructions': '1. Start standing\n2. Drop to push-up\n3. Return to standing\n4. Jump with arms overhead',
                'target_muscles': 'Full Body',
                'equipment_required': 'None',
                'difficulty_level': 'intermediate',
                'exercise_type': 'cardio'
            },
            {
                'name': 'Mountain Climbers',
                'description': 'Dynamic core and cardio exercise.',
                'instructions': '1. Start in plank\n2. Alternate bringing knees to chest\n3. Keep hips level\n4. Maintain quick pace',
                'target_muscles': 'Core, Shoulders, Hip Flexors',
                'equipment_required': 'None',
                'difficulty_level': 'intermediate',
                'exercise_type': 'cardio'
            },
            {
                'name': 'Box Jumps',
                'description': 'Plyometric exercise for explosive power.',
                'instructions': '1. Stand facing box\n2. Jump onto box\n3. Stand fully\n4. Step back down',
                'target_muscles': 'Legs, Core',
                'equipment_required': 'Plyo Box',
                'difficulty_level': 'intermediate',
                'exercise_type': 'cardio'
            },
            {
                'name': 'Battle Ropes',
                'description': 'High-intensity upper body conditioning.',
                'instructions': '1. Hold rope ends\n2. Create wave patterns\n3. Maintain intensity\n4. Vary movements',
                'target_muscles': 'Arms, Shoulders, Core',
                'equipment_required': 'Battle Ropes',
                'difficulty_level': 'intermediate',
                'exercise_type': 'cardio'
            }
        ]

        for exercise_data in exercises:
            Exercise.objects.get_or_create(**exercise_data)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(exercises)} exercises'))

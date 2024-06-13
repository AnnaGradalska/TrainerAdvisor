
class CustomizedExercises:
    TABLE_NAME = "customized_exercises"

    def __init__(self, wor_id, name, reps, sets, desc=None):
        self.wor_id = wor_id
        self.name = name
        self.reps = reps
        self.sets = sets
        self.desc = desc
        self.id = None

    @staticmethod
    def add_multiple_customized_exercises_to_db(db_manager, exercises):
        values_list = []

        for exe in exercises:
            values = {
                'cus_wor_id': exe[0],
                'cus_name': exe[1],
                'cus_reps': exe[2],
                'cus_sets': exe[3],
                'cus_desc': exe[4]
            }
            values_list.append(values)

        result = db_manager.add_multiple_data(CustomizedExercises.TABLE_NAME, values_list)

        if not result:
            return False

        return True

    def delete_customized_exercise_from_db(self, db_manager):
        db_manager.delete_data(self.TABLE_NAME, self.id)

    @staticmethod
    def get_customized_exercises_for_trainee(values, db_manager):
        result = db_manager.get_data(CustomizedExercises.TABLE_NAME, "cus_wor_id", values)

        if not result:
            return False

        return result

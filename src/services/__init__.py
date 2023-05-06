from config import PERIODS_PER_YEAR
from services.file_manager_service import FileManagerService
from services.planner_service import PlannerService

planner_service = PlannerService(PERIODS_PER_YEAR)
file_manager_service = FileManagerService()

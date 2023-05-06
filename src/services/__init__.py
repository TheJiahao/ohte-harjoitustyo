from config import PERIODS_PER_YEAR
from services.file_manager_service import FileManagerService
from services.planner_service import PlannerService
from services.scheduler_service import SchedulerService


scheduler_service = SchedulerService([])
file_manager_service = FileManagerService()
planner_service = PlannerService(PERIODS_PER_YEAR)

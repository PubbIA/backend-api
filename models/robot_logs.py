import uuid
from sqlalchemy import Column, String, Numeric, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship,Session
from database import Base
import datetime
from typing import List


class RobotLog(Base):
    __tablename__ = 'robot_logs'
    id = Column(String(37), primary_key=True, default=lambda: str(uuid.uuid4()))
    robot_id = Column(String(37), ForeignKey('robots.id'), nullable=False)
    operation = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    details = Column(String(255))

    robot = relationship("Robot", back_populates="logs")


    @classmethod
    def create_log(cls, session, robot_id: str, operation: str, details: float) -> bool:
        # Check if a robot with the given name already exists
        log_entry = cls(
            robot_id=robot_id,
            operation=operation,
            details=details
        )
        # Add the robot to the database
        session.add(log_entry)
        session.commit()
        return True
    @classmethod
    def get_all_logs(cls, session: Session) -> List['RobotLog']:
        return session.query(cls).all()

    @classmethod
    def get_logs_by_robot_id(cls, session: Session, robot_id: str) -> List['RobotLog']:
        return session.query(cls).filter(cls.robot_id == robot_id).all()

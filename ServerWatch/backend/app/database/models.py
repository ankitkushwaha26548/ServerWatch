from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from datetime import datetime

from .connection import Base


class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    hostname = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    operating_system = Column(String, nullable=False)
    status = Column(String, default="offline")
    last_seen = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ServerMetric(Base):
    __tablename__ = "server_metrics"

    id = Column(Integer, primary_key=True, index=True)

    server_id = Column(
        Integer,
        ForeignKey("servers.id"),
        nullable=False,
        index=True
    )

    cpu_usage = Column(Float, nullable=False)

    memory_usage = Column(Float, nullable=False)

    disk_usage = Column(Float, nullable=False)

    network_sent_mb = Column(Float, nullable=False)

    network_received_mb = Column(Float, nullable=False)

    uptime_seconds = Column(Integer, nullable=False)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )

class ApiEndpoint(Base):
    __tablename__ = "api_endpoints"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    url = Column(
        String,
        nullable=False
    )

    method = Column(
        String,
        default="GET"
    )

    status = Column(
        String,
        default="unknown"
    )

    last_status_code = Column(
        Integer,
        nullable=True
    )

    last_response_time = Column(
        Float,
        nullable=True
    )

    last_checked = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class ApiCheck(Base):
    __tablename__ = "api_checks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    api_id = Column(
        Integer,
        ForeignKey("api_endpoints.id"),
        nullable=False,
        index=True
    )

    status_code = Column(
        Integer,
        nullable=True
    )

    response_time = Column(
        Float,
        nullable=True
    )

    status = Column(
        String,
        nullable=False
    )

    error_message = Column(
        String,
        nullable=True
    )

    checked_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    api_id = Column(
        Integer,
        ForeignKey("api_endpoints.id"),
        nullable=True,
        index=True
    )

    alert_type = Column(
        String,
        nullable=False
    )

    message = Column(
        String,
        nullable=False
    )

    severity = Column(
        String,
        default="warning"
    )

    is_resolved = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )

    resolved_at = Column(
        DateTime,
        nullable=True
    )

class ServerLog(Base):
    __tablename__ = "server_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    server_id = Column(
        Integer,
        ForeignKey("servers.id"),
        nullable=False,
        index=True
    )

    level = Column(
        String,
        nullable=False
    )

    message = Column(
        String,
        nullable=False
    )

    source = Column(
        String,
        default="agent"
    )

    timestamp = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        default="USER",
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class Deployment(Base):
    __tablename__ = "deployments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    version = Column(
        String,
        nullable=False
    )

    environment = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )

    commit_hash = Column(
        String,
        nullable=False
    )

    deployed_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )
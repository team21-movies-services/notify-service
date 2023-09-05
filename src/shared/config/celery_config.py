from shared.enums.queues import QueueEnum

task_default_queue = QueueEnum.default

task_queues = {
    QueueEnum.instant: {'exchange': QueueEnum.instant, 'routing_key': QueueEnum.instant},
}

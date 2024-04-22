from rich.progress import Progress, BarColumn, TextColumn


def create_progress_bar(console):
    """
    Initializes and returns a progress bar for tracking task completion.

    Args:
        task_description (str): Description of the task for which progress is being tracked.
        total_items (int): The total number of items the progress bar needs to track.

    Returns:
        A rich.progress.Progress object initialized with the specified task and total items.
    """
    progress = Progress(
        "[progress.description]{task.description}",
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TextColumn("[green]{task.completed} of {task.total}"),
        console=console,
    )
    return progress

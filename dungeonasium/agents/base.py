from gymnasium import vector


class BaseAgent:
    def __init__(self,
                 env: vector.AsyncVectorEnv | vector.SyncVectorEnv) -> None:
        self.env = env

    @property
    def render_mode(self):
        """
        Shortcut to render_mode kwarg.

        Returns:
            str: render_mode
        """
        return self.env.spec.kwargs["render_mode"]

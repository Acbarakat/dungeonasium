from gymnasium import vector


class BaseAgent:
    def __init__(self,
                 env: vector.AsyncVectorEnv | vector.SyncVectorEnv,
                 seed: float | None = None) -> None:
        self.env = env
        self.seed = seed
        self.env.reset(seed=seed)

    @property
    def render_mode(self) -> str:
        """
        Shortcut to render_mode kwarg.

        Returns:
            str: render_mode
        """
        return self.env.spec.kwargs.get("render_mode", None)

    def swap_environments(self,
                          env: vector.AsyncVectorEnv | vector.SyncVectorEnv) -> None:
        self.env.close()
        self.env = env
        self.env.reset(seed=self.seed)

    def save(self):
        raise NotImplementedError()

    def load(self):
        raise NotImplementedError()

import logging, json
import db
from pathlib import Path
from string import Template

VIEWS_DIR = Path(__file__).parent / "views"

def _escape(value):
    return json.dumps(str(value))[1:-1]

logger = logging.getLogger(__name__)

class RenderTemplate:

    def __init__(self, client):
        self.client = client
        self._cache = {}


    def _render_view(self, view, user_id):
        logger.debug(f"Rendering view for {user_id}: {view}")
        try:
            self.client.views_publish(
                user_id=user_id,
                view=view
            )
            return True
        except Exception as e:
            logger.error(f"Error publishing view: {e}")
            return False

    def _get_view(self, surface, view_name, **values):
        cache_key = (surface, view_name)
        if cache_key not in self._cache:
            path = VIEWS_DIR / surface / f"{view_name}.json"
            self._cache[cache_key] = path.read_text(encoding="utf-8")

        raw = self._cache[cache_key]
        if values:
            raw = Template(raw).safe_substitute(
                {k: _escape(v) for k, v in values.items()}
            )
        return json.loads(raw)



    def render_home_tab(self, user_id):
        if db.methods.get_user(user_id):
            view = self._get_view("home", "onboarding") #should be replaced with dashboard when that's created
        else:
            view = self._get_view("home", "onboarding")

        return self._render_view(view, user_id)
from streamlit_elements import mui
from .dashboard import Dashboard



class Card(Dashboard.Item):
    DEFAULT_TITLE = "Shrimp and Chorizo Paella"
    DEFAULT_SUBHEADER = "September 14, 2016"
    DEFAULT_IMAGE = "https://mui.com/static/images/cards/paella.jpg"
    DEFAULT_CONTENT = (
        "This impressive paella is a perfect party dish and a fun meal to cook "
        "together with your guests. Add 1 cup of frozen peas along with the mussels, "
        "if you like."
    )
    
    def __init__(self, board, x, y, w, h, title=DEFAULT_TITLE, subheader=DEFAULT_SUBHEADER, image=DEFAULT_IMAGE, content=DEFAULT_CONTENT, **item_props):
        super().__init__(board, x, y, w, h, **item_props)
        self.title = title
        self.subheader = subheader
        self.image = image
        self.content = content

    def __call__(self, content=None):
        if content is not None:
            self.content = content
            
        with mui.Card(key=self._key, sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=1):
            mui.CardHeader(
                title=self.title,
                subheader=self.subheader,
                avatar=mui.Avatar(self.title[0], sx={"bgcolor": "red"}),  # Assumes first letter of title
                action=mui.IconButton(mui.icon.MoreVert),
                className=self._draggable_class,
            )
            mui.CardMedia(
                component="img",
                height=194,
                image=self.image,
                alt=f"{self.title} image",
            )

            with mui.CardContent(sx={"flex": 1}):
                mui.Typography(self.content)

            with mui.CardActions(disableSpacing=True):
                mui.IconButton(mui.icon.Favorite)
                mui.IconButton(mui.icon.Share)
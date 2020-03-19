from guillotina.behaviors.properties import ContextProperty
from guillotina.behaviors.instance import AnnotationBehavior
from guillotina.interfaces import IResource
from guillotina import configure, schema
from zope.interface import Interface

class IMySocketBehavior(Interface):
    websocket = schema.List(
        title="WebSocketList", 
        description="The list of opened socket"
    )

class ISocketMarcker(Interface):
    """Marker interface for content with attachment."""

@configure.behavior(
    title="Socket Attachmant",
    provides=IMySocketBehavior,
    marker=ISocketMarcker,
    for_=IResource)
class MySocketBehavior(AnnotationBehavior):
    """If attributes
    """
    websocket = ContextProperty("websocket", ())

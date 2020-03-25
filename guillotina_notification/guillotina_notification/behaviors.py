from guillotina.behaviors.properties import ContextProperty
from guillotina.behaviors.instance import AnnotationBehavior
from guillotina.interfaces import IResource
from guillotina import configure, schema
from zope.interface import Interface

class IMySocketBehavior(Interface):
    socket_urls = schema.Tuple(
        title="Socket_urls",
        description="The request used by the prepare() function",
        value_type=schema.TextLine(),
        required=False,
        naive=True,
        max_length=1000,
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
    socket_urls = ContextProperty("socket_urls", ())

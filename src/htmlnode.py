
class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list["HTMLNode"] | None = None, props: dict[str, str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self) -> str:
        if self.props is None or self.props == {}:
            return ""
        attributes = ""
        for key, value in self.props.items():
            attributes += f" {key}=\"{value}\""
        return attributes

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("invalid HTML: no value")

        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: ParentNode must have a child value")
        return self.to_html_r(self.children)

    def to_html_r(self, children: list[HTMLNode]) -> str:
        render_html = f"<{self.tag}{self.props_to_html()}>"
        for child in children:
            render_html += child.to_html()
        return render_html + f"</{self.tag}>"

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

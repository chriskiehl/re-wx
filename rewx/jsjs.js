const FeactInstanceMap = {
    set(key, value) {
        key.__feactInternalInstance = value;
    },

    get(key) {
        return key.__feactInternalInstance;
    }
};

class FeactDOMComponent {
    constructor(element) {
        this._currentElement = element;
    }

    mountComponent(container) {
        const domElement = document.createElement(this._currentElement.type);
        const textNode = document.createTextNode(this._currentElement.props.children);

        domElement.appendChild(textNode);
        container.appendChild(domElement);

        this._hostNode = domElement;
        return domElement;
    }

    receiveComponent(nextElement) {
        const prevElement = this._currentElement;
        this.updateComponent(prevElement, nextElement);
    }

    updateComponent(prevElement, nextElement) {
        const lastProps = prevElement.props;
        const nextProps = nextElement.props;

        this._updateDOMProperties(lastProps, nextProps);
        this._updateDOMChildren(lastProps, nextProps);
    }

    _updateDOMProperties(lastProps, nextProps) {
        // nothing to do! I'll explain why below
    }

    _updateDOMChildren(lastProps, nextProps) {
        const lastContent = lastProps.children;
        const nextContent = nextProps.children;

        if (!nextContent) {
            this.updateTextContent('');
        } else if (lastContent !== nextContent) {
            this.updateTextContent('' + nextContent);
        }
    }

    updateTextContent(content) {
        const node = this._hostNode;
        node.textContent = content;

        const firstChild = node.firstChild;

        if (firstChild && firstChild === node.lastChild
            && firstChild.nodeType === 3) {
            firstChild.nodeValue = content;
            return;
        }

        node.textContent = content;
    }
}

class FeactCompositeComponentWrapper {
    constructor(element) {
        this._currentElement = element;
    }

    mountComponent(container) {
        const Component = this._currentElement.type;
        const componentInstance = new Component(this._currentElement.props);
        this._instance = componentInstance;

        FeactInstanceMap.set(componentInstance, this);

        if (componentInstance.componentWillMount) {
            componentInstance.componentWillMount();
        }

        const markup = this.performInitialMount(container);

        if (componentInstance.componentDidMount) {
            componentInstance.componentDidMount();
        }

        return markup;
    }

    performInitialMount(container) {
        const renderedElement = this._instance.render();

        const child = instantiateFeactComponent(renderedElement);
        this._renderedComponent = child;

        return FeactReconciler.mountComponent(child, container);
    }

    performUpdateIfNecessary() {
        this.updateComponent(this._currentElement, this._currentElement);
    }

    receiveComponent(nextElement) {
        const prevElement = this._currentElement;
        this.updateComponent(prevElement, nextElement);
    }

    updateComponent(prevElement, nextElement) {
        this._updating = true;
        const nextProps = nextElement.props;
        const inst = this._instance;

        const willReceive = prevElement !== nextElement;

        if (willReceive && inst.componentWillReceiveProps) {
            inst.componentWillReceiveProps(nextProps);
        }

        let shouldUpdate = true;

        const nextState = this._processPendingState();

        if (inst.shouldComponentUpdate) {
            shouldUpdate = inst.shouldComponentUpdate(nextProps, nextState);
        }

        if (shouldUpdate) {
            this._performComponentUpdate(nextElement, nextProps, nextState);
        } else {
            inst.props = nextProps;
        }

        this._updating = false;
    }

    _processPendingState() {
        const inst = this._instance;
        if (!this._pendingPartialState) {
            return inst.state;
        }

        let nextState = inst.state;

        for (let i = 0; i < this._pendingPartialState.length; ++i) {
            nextState = Object.assign({}, nextState, this._pendingPartialState[i]);
        }

        this._pendingPartialState = null;
        return nextState;
    }

    _performComponentUpdate(nextElement, nextProps, nextState) {
        this._currentElement = nextElement;
        const inst = this._instance;

        inst.props = nextProps;
        inst.state = nextState;

        this._updateRenderedComponent();
    }

    _updateRenderedComponent() {
        const prevComponentInstance = this._renderedComponent;
        const inst = this._instance;
        const nextRenderedElement = inst.render();

        FeactReconciler.receiveComponent(prevComponentInstance, nextRenderedElement);
    }
}

const TopLevelWrapper = function (props) {
    this.props = props;
};

TopLevelWrapper.prototype.render = function () {
    return this.props;
};

function instantiateFeactComponent(element) {
    if (typeof element.type === 'string') {
        return new FeactDOMComponent(element);
    } else if (typeof element.type === 'function') {
        return new FeactCompositeComponentWrapper(element);
    }
}

const FeactReconciler = {
    mountComponent(internalInstance, container) {
        return internalInstance.mountComponent(container);
    },

    receiveComponent(internalInstance, nextElement) {
        internalInstance.receiveComponent(nextElement);
    },

    performUpdateIfNecessary(internalInstance) {
        internalInstance.performUpdateIfNecessary();
    }
};

function FeactComponent() {
}

FeactComponent.prototype.setState = function (partialState) {
    const internalInstance = FeactInstanceMap.get(this);
    internalInstance._pendingPartialState = internalInstance._pendingPartialState || [];
    internalInstance._pendingPartialState.push(partialState);

    if (!internalInstance._updating) {
        FeactReconciler.performUpdateIfNecessary(internalInstance);
    }
}

function mixSpecIntoComponent(Constructor, spec) {
    const proto = Constructor.prototype;

    for (const key in spec) {
        proto[key] = spec[key];
    }
}

const Feact = {
    createElement(type, props, children) {
        const element = {
            type,
            props: props || {}
        };

        if (children) {
            element.props.children = children;
        }

        return element;
    },

    createClass(spec) {
        function Constructor(props) {
            this.props = props;

            const initialState = this.getInitialState ? this.getInitialState() : null;
            this.state = initialState;
        }

        Constructor.prototype = new FeactComponent();

        mixSpecIntoComponent(Constructor, spec);

        return Constructor;
    },

    render(element, container) {
        const prevComponent = getTopLevelComponentInContainer(container);

        if (prevComponent) {
            return updateRootComponent(prevComponent, element);
        } else {
            return renderNewRootComponent(element, container);
        }
    }
};

function getTopLevelComponentInContainer(container) {
    return container.__feactComponentInstance;
}

function renderNewRootComponent(element, container) {
    const wrapperElement = Feact.createElement(TopLevelWrapper, element);
    const componentInstance = new FeactCompositeComponentWrapper(wrapperElement);

    const markUp = FeactReconciler.mountComponent(componentInstance, container);
    container.__feactComponentInstance = componentInstance._renderedComponent;

    return markUp;
}

function updateRootComponent(prevComponent, nextElement) {
    FeactReconciler.receiveComponent(prevComponent, nextElement);
}

const MyComponent = Feact.createClass({
    componentWillMount() {
        this.renderCount = 0;
    },

    getInitialState() {
        return {
            message: 'state from getInitialState'
        };
    },

    componentWillReceiveProps(nextProps) {
        this.setState({message: 'state from componentWillReceiveProps'});
    },

    render() {
        this.renderCount += 1;
        return Feact.createElement('h1', null, 'this is render ' + this.renderCount + ', with state: ' + this.state.message + ', and this prop: ' + this.props.prop);
    }
});

Feact.render(
    Feact.createElement(MyComponent, {prop: 'first prop'}),
    document.getElementById('root')
);

setTimeout(function () {
    Feact.render(
        Feact.createElement(MyComponent, {prop: 'second prop'}),
        document.getElementById('root')
    );
}, 10000);




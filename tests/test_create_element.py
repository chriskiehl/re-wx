from unittest import TestCase

from rewx.rewx2 import create_element, wsx


class TestCreateElement(TestCase):

    def test_create_element(self):

        element = create_element('foo', {'bar': 'baz'})
        self.assertEqual(element, {
            'type': 'foo',
            'props': {'bar': 'baz'},
        })
        # children key not present in props if not supplied
        self.assertNotIn('children', element['props'])


        # when supplied, `children` get added to props
        element = create_element('foo', {'bar': 'baz'}, children=[
            create_element('some-elm', {'some': 'value'})
        ])
        self.assertEqual(element, {
            'type': 'foo',
            'props': {
                'bar': 'baz',
                'children': [{
                    'type': 'some-elm',
                    'props': {'some': 'value'}
                }]
            }
        })

    def test_wsx(self):
        # calling as function
        result = wsx(['foo', {'bar': 'baz'}])
        self.assertEqual(result, create_element('foo', {'bar': 'baz'}))


        @wsx
        def my_component(props):
            return ['foo', props]

        # asserting the function name gets @wrapped correctly
        self.assertEqual(my_component.__name__, 'my_component')

        self.assertEqual(my_component({'bar': 'baz'}), create_element('foo', {'bar': 'baz'}))


    def test_too(self):
        #TODO: some of these cases can only be tested once things get mounted
        @wsx
        def comp_b(props):
            return ['b', {'bar': props['from_comp_a']}, props.get('children')]

        @wsx
        def comp_a(props):
            return [comp_a, {'from_comp_a': 'hello!'},
                    ['child1', {}],
                    ['child2', {}]]

        print(comp_a({'uhh':'what'}))
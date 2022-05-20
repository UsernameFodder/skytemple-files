# mypy: ignore-errors

from itertools import chain
from typing import TYPE_CHECKING, Container, Iterable, Tuple, Union, Any

from astroid import nodes
from pylint.checkers import BaseChecker, utils
from pylint.checkers.deprecated import ACCEPTABLE_NODES
from pylint.checkers.utils import get_import_name, infer_all, safe_infer
from pylint.interfaces import IAstroidChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class DeprecationChecker(BaseChecker):
    """
    Class implementing deprecation checker.

    This is forked from the DeprecatedMixin, since it isn't working:
    https://github.com/PyCQA/pylint/issues/6656
    """
    __implements__ = (IAstroidChecker,)
    name = "deprecated-function-call-st"
    options = ()
    enabled = True
    msgs = {
        "W9905": (
            "Using deprecated method %s()",
            "deprecated-method-st",
            "The method is marked as deprecated and will be removed in the future.",
        ),
        "W9911": (
            "Using deprecated argument %s of method %s()",
            "deprecated-argument-st",
            "The argument is marked as deprecated and will be removed in the future.",
        ),
        "W9902": (
            "Uses of a deprecated module %r",
            "deprecated-module-st",
            "A module marked as deprecated is imported.",
        ),
        "W9912": (
            "Using deprecated class %s of module %s",
            "deprecated-class-st",
            "The class is marked as deprecated and will be removed in the future.",
        ),
        "W9913": (
            "Using deprecated decorator %s()",
            "deprecated-decorator-st",
            "The decorator is marked as deprecated and will be removed in the future.",
        ),
    }

    @utils.check_messages(
        "deprecated-method-st",
        "deprecated-argument-st",
        "deprecated-class-st",
    )
    def visit_call(self, node: nodes.Call) -> None:
        """Called when a :class:`nodes.Call` node is visited."""
        self.check_deprecated_class_in_call(node)
        for inferred in infer_all(node.func):
            # Calling entry point for deprecation check logic.
            self.check_deprecated_method(node, inferred)

    @utils.check_messages(
        "deprecated-module-st",
        "deprecated-class-st",
    )
    def visit_import(self, node: nodes.Import) -> None:
        """Triggered when an import statement is seen."""
        for name in (name for name, _ in node.names):
            self.check_deprecated_module(node, name)
            if "." in name:
                # Checking deprecation for import module with class
                mod_name, class_name = name.split(".", 1)
                self.check_deprecated_class(node, mod_name, (class_name,))

    def deprecated_decorators(self) -> Iterable:
        """Callback returning the deprecated decorators.

        Returns:
            collections.abc.Container of deprecated decorator names.
        """
        # pylint: disable=no-self-use
        return ()

    @utils.check_messages("deprecated-decorator-st")
    def visit_decorators(self, node: nodes.Decorators) -> None:
        """Triggered when a decorator statement is seen."""
        children = list(node.get_children())
        if not children:
            return
        if isinstance(children[0], nodes.Call):
            inf = safe_infer(children[0].func)
        else:
            inf = safe_infer(children[0])
        qname = inf.qname() if inf else None
        if qname in self.deprecated_decorators():
            self.add_message("deprecated-decorator-st", node=node, args=qname)

    @utils.check_messages(
        "deprecated-module-st",
        "deprecated-class-st",
    )
    def visit_importfrom(self, node: nodes.ImportFrom) -> None:
        """Triggered when a from statement is seen."""
        basename = node.modname
        basename = get_import_name(node, basename)
        self.check_deprecated_module(node, basename)
        class_names = (name for name, _ in node.names)
        self.check_deprecated_class(node, basename, class_names)

    def deprecated_methods(self) -> Container[str]:
        """Callback returning the deprecated methods/functions.

        Returns:
            collections.abc.Container of deprecated function/method names.
        """
        # pylint: disable=no-self-use
        return {
            "skytemple_files.common.util.read_uintle",
            "skytemple_files.common.util.read_uintbe",
            "skytemple_files.common.util.read_sintle",
            "skytemple_files.common.util.read_sintbe",
            "skytemple_files.common.util.write_uintle",
            "skytemple_files.common.util.write_uintbe",
            "skytemple_files.common.util.write_sintle",
            "skytemple_files.common.util.write_sintbe",
        }

    def deprecated_arguments(
        self, method: str
    ) -> Iterable[Tuple[Union[int, None], str]]:
        """Callback returning the deprecated arguments of method/function.

        Args:
            method (str): name of function/method checked for deprecated arguments

        Returns:
            collections.abc.Iterable in form:
                ((POSITION1, PARAM1), (POSITION2: PARAM2) ...)
            where
                * POSITIONX - position of deprecated argument PARAMX in function definition.
                  If argument is keyword-only, POSITIONX should be None.
                * PARAMX - name of the deprecated argument.
            E.g. suppose function:

            .. code-block:: python
                def bar(arg1, arg2, arg3, arg4, arg5='spam')

            with deprecated arguments `arg2` and `arg4`. `deprecated_arguments` should return:

            .. code-block:: python
                ((1, 'arg2'), (3, 'arg4'))
        """
        # pylint: disable=no-self-use
        # pylint: disable=unused-argument
        return ()

    def deprecated_modules(self) -> Iterable:
        """Callback returning the deprecated modules.

        Returns:
            collections.abc.Container of deprecated module names.
        """
        # pylint: disable=no-self-use
        return ()

    def deprecated_classes(self, module: str) -> Iterable:
        """Callback returning the deprecated classes of module.

        Args:
            module (str): name of module checked for deprecated classes

        Returns:
            collections.abc.Container of deprecated class names.
        """
        # pylint: disable=no-self-use
        # pylint: disable=unused-argument
        return ()

    def check_deprecated_module(self, node, mod_path):
        """Checks if the module is deprecated."""
        for mod_name in self.deprecated_modules():
            if mod_path == mod_name or mod_path.startswith(mod_name + "."):
                self.add_message("deprecated-module-st", node=node, args=mod_path)

    def check_deprecated_method(self, node, inferred):
        """Executes the checker for the given node.

        This method should be called from the checker implementing this mixin.
        """

        # Reject nodes which aren't of interest to us.
        if not isinstance(inferred, ACCEPTABLE_NODES):
            return

        if isinstance(node.func, nodes.Attribute):
            func_name = node.func.attrname
        elif isinstance(node.func, nodes.Name):
            func_name = node.func.name
        else:
            # Not interested in other nodes.
            return

        if hasattr(inferred.parent, "qname") and inferred.parent.qname():
            # Handling the situation when deprecated function is
            # alias to existing function.
            qnames = {
                inferred.qname(),
                f"{inferred.parent.qname()}.{func_name}",
                func_name,
            }
        else:
            qnames = {inferred.qname(), func_name}
        if any(name in self.deprecated_methods() for name in qnames):
            self.add_message("deprecated-method-st", node=node, args=(func_name,))
            return
        num_of_args = len(node.args)
        kwargs = {kw.arg for kw in node.keywords} if node.keywords else {}
        deprecated_arguments = (self.deprecated_arguments(qn) for qn in qnames)
        for position, arg_name in chain(*deprecated_arguments):
            if arg_name in kwargs:
                # function was called with deprecated argument as keyword argument
                self.add_message(
                    "deprecated-argument-st", node=node, args=(arg_name, func_name)
                )
            elif position is not None and position < num_of_args:
                # function was called with deprecated argument as positional argument
                self.add_message(
                    "deprecated-argument-st", node=node, args=(arg_name, func_name)
                )

    def check_deprecated_class(self, node, mod_name, class_names):
        """Checks if the class is deprecated."""

        for class_name in class_names:
            if class_name in self.deprecated_classes(mod_name):
                self.add_message(
                    "deprecated-class-st", node=node, args=(class_name, mod_name)
                )

    def check_deprecated_class_in_call(self, node):
        """Checks if call the deprecated class."""

        if isinstance(node.func, nodes.Attribute) and isinstance(
            node.func.expr, nodes.Name
        ):
            mod_name = node.func.expr.name
            class_name = node.func.attrname
            self.check_deprecated_class(node, mod_name, (class_name,))


def register(linter: 'PyLinter') -> None:
    linter.register_checker(DeprecationChecker(linter))

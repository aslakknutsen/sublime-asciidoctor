import re
import sublime
import sublime_plugin
import webbrowser


REG_RENAME = re.compile("\.(asciidoc|adoc|asc|ad)$")
EXT = re.compile(".*\.(asciidoc|adoc|asc|ad)$")
COMMAND = "asciidoctor -a linkcss! -a data-uri -a source-highlighter=highlightjs"


def is_asciidoc_file(file_name):
    return EXT.match(file_name) is not None


class AsciidocSaveListener(sublime_plugin.EventListener):

    def on_post_save(self, view):
        file_name = view.file_name()
        if is_asciidoc_file(file_name):
            sublime.status_message("Asciidoctor regenerating " + file_name)
            self.run_shell_command(view, COMMAND + " " + file_name)

    def run_shell_command(self, view, command):
        if not command:
            return False
        view.window().run_command("exec", {
            "cmd": [command],
            "shell": True,
            "quiet": True
        })
        return True


class AsciidocBrowserCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file_name = self.view.file_name()
        if is_asciidoc_file(file_name):
            webbrowser.open_new(REG_RENAME.sub('.html', file_name))

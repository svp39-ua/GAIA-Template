import { useEditor, EditorContent } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'
import { cn } from '@/lib/utils'

interface TiptapEditorProps {
    value: string
    onChange: (value: string) => void
    disabled?: boolean
}

export function TiptapEditor({ value, onChange, disabled }: TiptapEditorProps) {
    const editor = useEditor({
        extensions: [StarterKit],
        content: value,
        editable: !disabled,
        onUpdate: ({ editor }) => {
            onChange(editor.getHTML())
        },
        editorProps: {
            attributes: {
                class: cn(
                    "min-h-[150px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 prose prose-sm max-w-none"
                ),
            },
        },
    })

    if (!editor) {
        return null
    }

    return (
        <div className="space-y-2">
            <div className="flex gap-2 border rounded-md p-1 bg-muted/20">
                <button
                    type="button"
                    onClick={() => editor.chain().focus().toggleBold().run()}
                    className={cn("px-2 py-1 text-sm rounded", editor.isActive('bold') ? 'bg-muted font-bold' : '')}
                >
                    Bold
                </button>
                <button
                    type="button"
                    onClick={() => editor.chain().focus().toggleItalic().run()}
                    className={cn("px-2 py-1 text-sm rounded", editor.isActive('italic') ? 'bg-muted italic' : '')}
                >
                    Italic
                </button>
                <button
                    type="button"
                    onClick={() => editor.chain().focus().toggleBulletList().run()}
                    className={cn("px-2 py-1 text-sm rounded", editor.isActive('bulletList') ? 'bg-muted' : '')}
                >
                    List
                </button>
            </div>
            <EditorContent editor={editor} />
        </div>
    )
}

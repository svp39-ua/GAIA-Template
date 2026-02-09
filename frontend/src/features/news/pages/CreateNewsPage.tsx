// [Feature: News Management] [Story: NM-ADM-001] [Ticket: NM-ADM-001-FE-T03]
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { useMutation } from "@tanstack/react-query"
import { createNews, type NewsCreatePayload } from "@/lib/news-service"
import { toast } from "sonner"
import { Button, Input, Label, Textarea } from "@/components/ui/primitives"
import { TiptapEditor } from "@/components/ui/tiptap-editor"
import { cn } from "@/lib/utils"

const newsSchema = z.object({
    title: z.string().min(1, "El título es obligatorio").max(255),
    summary: z.string().max(500, "El resumen no puede exceder 500 caracteres").optional(),
    content: z.string().optional(),
    scope: z.enum(["GENERAL", "INTERNAL"]),
    cover_url: z.string().url("Debe ser una URL válida").optional().or(z.literal("")),
})

type NewsFormValues = z.infer<typeof newsSchema>

export default function CreateNewsPage() {
    const {
        register,
        handleSubmit,
        setValue,
        watch,
        reset,
        formState: { errors, isSubmitting },
    } = useForm<NewsFormValues>({
        resolver: zodResolver(newsSchema),
        defaultValues: {
            scope: "GENERAL",
            content: "",
            cover_url: ""
        },
    })

    // Watch content for manual validation if needed, or pass to editor
    const contentValue = watch("content") || ""

    const mutation = useMutation({
        mutationFn: createNews,
        onSuccess: () => {
            toast.success("Noticia creada exitosamente")
            reset()
        },
        onError: (error) => {
            toast.error("Error al crear la noticia")
            console.error(error)
        },
    })

    const onSubmit = (data: NewsFormValues) => {
        const payload: NewsCreatePayload = {
            title: data.title,
            summary: data.summary,
            content: data.content,
            scope: data.scope,
            cover_url: data.cover_url || undefined
        }
        mutation.mutate(payload)
    }

    return (
        <div className="max-w-3xl mx-auto p-6 space-y-8">
            <div>
                <h1 className="text-3xl font-bold tracking-tight text-primary">Crear Noticia</h1>
                <p className="text-muted-foreground">Publique una nueva comunicación para la comunidad.</p>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6 border p-6 rounded-lg bg-card shadow-sm">

                {/* TITLE */}
                <div className="space-y-2">
                    <Label htmlFor="title">Título *</Label>
                    <Input id="title" placeholder="Ej: Importante: Reunión Anual" {...register("title")} />
                    {errors.title && <p className="text-sm text-destructive">{errors.title.message}</p>}
                </div>

                {/* SUMMARY */}
                <div className="space-y-2">
                    <Label htmlFor="summary">Resumen</Label>
                    <Textarea
                        id="summary"
                        placeholder="Breve descripción que aparecerá en la lista..."
                        className="h-20"
                        {...register("summary")}
                    />
                    {errors.summary && <p className="text-sm text-destructive">{errors.summary.message}</p>}
                </div>

                {/* CONTENT (TIPTAP) */}
                <div className="space-y-2">
                    <Label>Contenido</Label>
                    <TiptapEditor
                        value={contentValue}
                        onChange={(val) => setValue("content", val, { shouldValidate: true })}
                    />
                </div>

                {/* SCOPE */}
                <div className="space-y-2">
                    <Label htmlFor="scope">Visibilidad</Label>
                    <select
                        id="scope"
                        className={cn(
                            "flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                        )}
                        {...register("scope")}
                    >
                        <option value="GENERAL">General (Público)</option>
                        <option value="INTERNAL">Interno (Solo Miembros)</option>
                    </select>
                </div>

                {/* COVER URL */}
                <div className="space-y-2">
                    <Label htmlFor="cover_url">URL Imagen de Portada</Label>
                    <Input id="cover_url" placeholder="https://..." {...register("cover_url")} />
                    {errors.cover_url && <p className="text-sm text-destructive">{errors.cover_url.message}</p>}
                </div>

                {/* ACTIONS */}
                <div className="flex justify-end gap-4 pt-4">
                    <Button type="button" variant="outline" onClick={() => window.history.back()}>Wait, Cancelar</Button>
                    <Button type="submit" disabled={isSubmitting || mutation.isPending}>
                        {mutation.isPending ? "Guardando..." : "Crear Noticia"}
                    </Button>
                </div>
            </form>
        </div>
    )
}

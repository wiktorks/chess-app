import { Navigation } from './Navigation'

interface LayoutProps {
    children: object
}

export const Layout = (props: LayoutProps) => {
    return (
        <>
            <Navigation />
            <main>{props.children}</main>
        </>
    )
}

// @ts-ignore
import returnToTopScript from "./scripts/returntotop.inline"
import styles from "./styles/returntotop.scss"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"

const ReturnToTop: QuartzComponent = ({ displayClass }: QuartzComponentProps) => {
  return (
    <button
      class={classNames(displayClass, "return-to-top")}
      id="return-to-top"
      aria-label="Return to top of page"
    >
      ↑
    </button>
  )
}

ReturnToTop.beforeDOMLoaded = returnToTopScript
ReturnToTop.css = styles

export default (() => ReturnToTop) satisfies QuartzComponentConstructor

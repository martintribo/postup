# PostupLifecycle

TLC reached 25 states and 55 steps. The chart draws 12 states and 18 arrows.
The chart does not draw 15 steps that stay in one chart state.
With VIEW, TLC keeps one representative for each group of states that it counts as the same. An arrow can lead to the representative rather than to the state that the step reaches.

## Rules that hold
TypeOK, NoJoinWhenClosed, EndedLinkNeverLive, AskOnlyWhenDelivered, FullOnlyWhenFillsDelivered, WayOutToEnded

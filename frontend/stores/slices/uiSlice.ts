import { createSlice } from "@reduxjs/toolkit";

type UiState = {
  sideBarOpen: boolean;
};
const initialState: UiState = {
  sideBarOpen: true,
};
const uiSlice = createSlice({
  name: "ui",
  initialState,
  reducers: {
    toggleSideBar: (state) => {
      state.sideBarOpen = !state.sideBarOpen;
    },
  },
});
export const { toggleSideBar } = uiSlice.actions;
export default uiSlice.reducer;
